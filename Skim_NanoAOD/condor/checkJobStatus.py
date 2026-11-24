#!/usr/bin/env python3
"""Incremental, parallel skim checks. Prepares retries; never submits jobs.

The submission archive is authoritative for input lists and job splitting.
Passed results are cached in JSON; subsequent rounds check unresolved jobs.
Final normalization export is deliberately a separate step.
"""
import argparse
import ast
import errno
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import multiprocessing as mp
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import time
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
YEARS = ("2016Pre", "2016Post", "2017", "2018")
SCHEMA = 1
LOG_SCHEMA = 2
ACTIVE = {1: "idle", 2: "running", 3: "removing", 5: "held", 6: "transferring", 7: "suspended"}


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(path, data):
    """Only the parent writes JSON; replace atomically, never leave partial JSON."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w") as handle:
        json.dump(data, handle, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def literals(text):
    values = {}
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign):
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue
            for name in node.targets:
                if isinstance(name, ast.Name):
                    values[name.id] = value
    return values


def canonical(name):
    path = urlsplit(name).path if "://" in name else name
    return "/store/" + path.split("/store/", 1)[1] if "/store/" in path else str(Path(path).absolute())


def split_files(files, total):
    if not 1 <= total <= len(files):
        raise ValueError("Invalid job count for input list")
    size, extra = divmod(len(files), total)
    start = 0
    result = []
    for index in range(total):
        end = start + size + (index < extra)
        result.append(files[start:end])
        start = end
    return result


def job_key(year, sample, number, total):
    return f"{year}/{sample}/{number}of{total}"


def manifest_for(args):
    submission = args.submission_dir.resolve()
    archive_path = submission / "Skim_NanoAOD.tar.gz"
    with tarfile.open(archive_path, "r:gz") as archive:
        def read(suffix):
            matches = [m for m in archive.getmembers() if m.isfile() and m.name.endswith("/" + suffix)]
            if len(matches) != 1:
                raise ValueError("Archive must contain exactly one " + suffix)
            return archive.extractfile(matches[0]).read().decode()
        files_text, jobs_text, config_text = (read(name) for name in
            ("sample/FilesNano_cff.sh", "sample/JobsNano_cff.py", "SkimInputs.py"))
    lists = dict(re.findall(r'^([A-Za-z_]\w*)="([^"\n]*)"[ \t]*$', files_text, re.MULTILINE))
    configs = literals(jobs_text)
    base = args.output_base or literals(config_text)["outSkimDir"]
    if base.startswith("/store/"):
        base = "root://cmseos.fnal.gov/" + base
    elif "://" not in base:
        base = str(Path(base).resolve())
    base = base.rstrip("/")
    jobs, samples, missing = {}, {}, set(args.samples or [])
    for year in args.years:
        for sample, values in configs["Samples_" + year].items():
            if args.samples and sample not in args.samples:
                continue
            missing.discard(sample)
            tokens = shlex.split(lists[f"{sample}_FileList_{year}"])
            if len(tokens) < 2 or tokens[0] not in ("local", "xrootd"):
                raise ValueError("Missing input mode or filenames for " + sample)
            files = [canonical(p) for p in tokens[1:]]
            if len(files) != len(set(files)):
                raise ValueError("Duplicate inputs for " + sample)
            total = int(values[0])
            sample_key = year + "/" + sample
            samples[sample_key] = {"year": year, "sample": sample, "is_mc": "Data" not in sample,
                "expected_jobs": total, "expected_input_events": int(values[2]),
                "expected_count_source": "DAS input-event total cached in submitted JobsNano_cff.py",
                "actual_input_files": len(files), "stored_input_files": int(values[3])}
            for number, assigned in enumerate(split_files(files, total), 1):
                name = f"{sample}_Skim_{number}of{total}.root"
                jobs[job_key(year, sample, number, total)] = {
                    "year": year, "sample": sample, "sample_key": sample_key, "number": number,
                    "total": total, "is_mc": "Data" not in sample, "inputs": assigned,
                    "filename": name, "output": f"{base}/{year}/{name}"}
    if missing or not jobs:
        raise ValueError("No matching jobs for samples: " + ", ".join(sorted(missing)))
    wrapper = submission / "runMakeSkims.sh"
    provenance = {"archive": str(archive_path), "archive_sha256": digest(archive_path.read_bytes()),
        "wrapper_sha256": digest(wrapper.read_bytes()), "output_base": base,
        "file_list_sha256": digest(files_text.encode()), "job_config_sha256": digest(jobs_text.encode())}
    content = {"schema_version": SCHEMA, "provenance": provenance, "samples": samples, "jobs": jobs}
    fingerprint = digest(json.dumps(content, sort_keys=True).encode())
    return dict(content, fingerprint=fingerprint)


def parse_args_line(text):
    match = re.search(r"^All argu?ments:\s*(.*)$", text, re.MULTILINE)
    if not match:  # Historical wrapper uses the spelling 'arguements'.
        match = re.search(r"^All arguements:\s*(.*)$", text, re.MULTILINE)
    if not match:
        return None
    parts = shlex.split(match[1])
    if len(parts) != 5 or parts[0] not in YEARS:
        return None
    year, sample, number, total, output_dir = parts
    try:
        number, total = int(number), int(total)
    except ValueError:
        return None
    return job_key(year, sample, number, total), output_dir


def bounded_text(path):
    if not path.exists():
        return ""
    with path.open("rb") as handle:
        head = handle.read(1024 * 1024)
        if path.stat().st_size > len(head):
            handle.seek(max(len(head), path.stat().st_size - 1024 * 1024))
            head += b"\n" + handle.read()
    return head.decode(errors="replace")


def attempts_for(directories, jobs, cache=None):
    result, updated = {}, {}
    cache = cache or {}
    paths = sorted({p for directory in directories for p in Path(directory).resolve().rglob("*.stdout")})
    def read_attempt(path):
        try:
            stderr = path.with_suffix(".stderr")
            stat = path.stat()
            err_stat = stderr.stat() if stderr.exists() else None
            signature = [stat.st_mtime_ns, stat.st_size,
                         err_stat.st_mtime_ns if err_stat else None, err_stat.st_size if err_stat else None]
            cached = cache.get(str(path))
            if cached and cached.get("signature") == signature and cached.get("parser_version") == LOG_SCHEMA:
                return str(path), cached
            text = bounded_text(path)
            parsed = parse_args_line(text)
            if not parsed or parsed[0] not in jobs:
                return str(path), {"signature": signature, "parser_version": LOG_SCHEMA, "key": None}
            key, output_dir = parsed
            job = jobs[key]
            expected_dir = job["output"].rsplit("/", 1)[0]
            if canonical(output_dir) != canonical(expected_dir):
                return str(path), {"signature": signature, "parser_version": LOG_SCHEMA, "key": None}
            errors = bounded_text(path.with_suffix(".stderr"))
            loaded = re.findall(r"^(?:Validated )?((?:root://|/store/)\S+?\.root)\s+(?:\((\d+) entries\)|(\d+))\s*$", text, re.MULTILINE)
            input_counts = re.findall(r"(?:Input events\s*=|Sample has)\s*(\d+)", text)
            cumulative = [(canonical(row[0]), int(row[2])) for row in loaded if row[2]]
            previous, entryless = 0, []
            for filename, count in cumulative:
                if count == previous:
                    entryless.append(filename)
                previous = count
            last = path.stat().st_mtime_ns
            attempt = {"stdout": str(path), "stderr": str(path.with_suffix(".stderr")),
                "condor_log": str(path.with_suffix(".condor")), "mtime_ns": last,
                "input_events_in_log": int(input_counts[-1]) if input_counts else None,
                "loaded_inputs": sorted(set(canonical(row[0]) for row in loaded)),
                "last_cumulative_entries": cumulative[-1][1] if cumulative else None,
                "entryless_inputs": entryless,
                "completed_skim": bool(re.search(r"nEvents_Skim\s*=\s*\d+", text)),
                "entryless_input_error": any(Path(filename).name in errors for filename in entryless),
                "error_lines": [line[:400] for line in errors.splitlines()
                    if re.search(r"error|fatal|killed|traceback|permission|truncated|zombie", line, re.I)][:12]}
            return str(path), {"signature": signature, "parser_version": LOG_SCHEMA, "key": key, "attempt": attempt}
        except FileNotFoundError:  # A just-started or rotated log can disappear during a scan.
            return str(path), None
    # Parallelize local/NFS log I/O, independently of the spawned ROOT workers.
    with ThreadPoolExecutor(max_workers=12) as executor:
        for index, (path, item) in enumerate(executor.map(read_attempt, paths), 1):
            if item:
                updated[path] = item
                if item["key"]:
                    result.setdefault(item["key"], []).append(item["attempt"])
            if index % 500 == 0:
                print(f"Indexed {index}/{len(paths)} logs", file=sys.stderr, flush=True)
    for values in result.values():
        values.sort(key=lambda a: (a["mtime_ns"], a["stdout"]))
    return result, updated


def run_json(command, timeout):
    options = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   text=True, timeout=timeout, check=True)
    try:
        result = subprocess.run(command, **options)
    except OSError as error:
        if error.errno != errno.ENOEXEC:
            raise
        # The LPC condor_q wrapper is shell text without a shebang. Interactive
        # shells handle ENOEXEC automatically; subprocess deliberately does not.
        executable = shutil.which(command[0]) or command[0]
        result = subprocess.run(["/bin/bash", executable, *command[1:]], **options)
    # With -schedd-constraint, the LPC client returns successful empty output
    # when every queried queue is empty. Do not accept empty error responses.
    if not result.stdout.strip() and not result.stderr.strip():
        return []
    if re.search(r"\b(error|failed|unable|could not|couldn't|cannot)\b", result.stderr, re.I):
        raise ValueError("Condor queue query reported errors: " + result.stderr[:1000])
    # A multi-schedd query may emit consecutive JSON arrays.
    text, ads = result.stdout.strip(), []
    decoder = json.JSONDecoder()
    while text:
        value, end = decoder.raw_decode(text)
        if not isinstance(value, list):
            raise ValueError("Expected a Condor ClassAd array")
        ads.extend(value)
        text = text[end:].lstrip()
    return ads


def queue_snapshot(args, jobs):
    try:
        ads = json.loads(args.queue_json.read_text()) if args.queue_json else run_json([
            "condor_q", "-json", "-attributes", "ClusterId,ProcId,JobStatus,Args,Arguments,Out,Err,UserLog"], args.io_timeout)
        if not isinstance(ads, list):
            raise ValueError("Unexpected condor_q response")
        active = {}
        for ad in ads:
            parsed = parse_args_line("All arguments: " + str(ad.get("Args", ad.get("Arguments", ""))))
            if parsed and parsed[0] in jobs and int(ad.get("JobStatus", 0)) in ACTIVE:
                key, out = parsed
                if canonical(out) == canonical(jobs[key]["output"].rsplit("/", 1)[0]):
                    active[key] = {"cluster": ad.get("ClusterId"), "process": ad.get("ProcId"),
                        "status": ACTIVE[int(ad["JobStatus"])], "stdout": ad.get("Out")}
        return active, None
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        # Never infer that missing jobs are safe to retry if queue lookup failed.
        return {}, str(error)


def inventories(manifest, timeout):
    result = {}
    base = manifest["provenance"]["output_base"]
    for year in sorted({j["year"] for j in manifest["jobs"].values()}):
        directory = f"{base}/{year}"
        if directory.startswith("root://"):
            url = urlsplit(directory)
            command = ["eos", f"root://{url.netloc}/", "ls", "/" + url.path.lstrip("/")]
            response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      text=True, timeout=timeout)
            if response.returncode:
                raise RuntimeError(f"EOS listing failed for {directory}: {response.stderr.strip()}")
            names = response.stdout.splitlines()
        else:
            names = [p.name for p in Path(directory).iterdir() if p.is_file()]
        result[year] = {Path(p).name for p in names if p.endswith(".root")}
    return result


def init_worker(timeout):
    # ROOT is initialized inside spawned children; no fork of ROOT's runtime.
    os.environ["XRD_CONNECTIONWINDOW"] = str(timeout)
    os.environ["XRD_REQUESTTIMEOUT"] = str(timeout)
    os.environ["XRD_STREAMTIMEOUT"] = str(timeout)
    os.environ["XRD_CONNECTIONRETRY"] = "1"
    import ROOT
    ROOT.gROOT.SetBatch(True)


def partial_attempt(latest, input_events):
    """Recognize a stale partial output without interpreting every warning as failure.

    Old TChain logs printed a cumulative count even when adding a file yielded
    no entries. Couple that evidence to an unfinished skim or an error naming
    that file, and require the EOS input counter to match the partial count.
    A repaired output with the complete counter is not rejected by stale logs.
    """
    return bool(latest and latest.get("entryless_inputs")
        and (not latest.get("completed_skim") or latest.get("entryless_input_error"))
        and input_events == latest.get("last_cumulative_entries"))


def input_count_cache(state_dir, source=None):
    path = state_dir / "input_event_counts.json"
    data = json.loads(path.read_text()) if path.exists() else {"schema_version": 1, "files": {}, "sources": []}
    if source:
        incoming = json.loads(source.read_text())
        for name, value in incoming["files"].items():
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError("Invalid expected input-event count: " + name)
            name = canonical(name)
            if name in data["files"] and data["files"][name] != value:
                raise ValueError("DAS input-event cache changed for " + name)
            data["files"][name] = value
        provenance = {"file": str(source.resolve()), "sha256": digest(source.read_bytes()), "added_utc": now()}
        if not any(p["sha256"] == provenance["sha256"] for p in data["sources"]):
            data["sources"].append(provenance)
        save(path, data)
    return data


def root_check(task):
    import ROOT
    key, job, latest = task
    result = {"status": "failed", "checked_utc": now(), "reason": None}
    handle = None
    try:
        handle = ROOT.TFile.Open(job["output"], "READ")
        if not handle or handle.IsZombie() or handle.TestBit(ROOT.TFile.kRecovered):
            raise ValueError("unreadable_or_recovered_root_file")
        tree = handle.Get("Events")
        if not tree or not tree.InheritsFrom("TTree"):
            raise ValueError("missing_Events_tree")
        for flag in ("passTrigMuTable9", "passTrigEleTable9"):
            leaf = tree.GetLeaf(flag)
            if not leaf or leaf.GetTypeName() != "Int_t":
                raise ValueError("missing_or_invalid_" + flag)
        hist = handle.Get("hEvents")
        if not hist or not hist.InheritsFrom("TH1") or hist.GetNbinsX() < 4:
            raise ValueError("missing_or_invalid_hEvents")
        counts = [float(hist.GetBinContent(i)) for i in (2, 3, 4)]
        if not all(math.isfinite(n) and n >= 0 and n.is_integer() for n in counts):
            raise ValueError("invalid_event_counters")
        input_events, filtered, selected = map(int, counts)
        if not input_events >= filtered >= selected or tree.GetEntries() != selected:
            raise ValueError("tree_entries_or_cutflow_mismatch")
        result.update(input_events=input_events, filtered_events=filtered, selected_events=selected,
                      root_entries=int(tree.GetEntries()), counter_class=hist.ClassName(),
                      file_size=int(handle.GetSize()), genEventCount=None, genEventSumw=None)
        expected = job.get("expected_input_events")
        result["expected_input_events"] = expected
        if job["is_mc"]:
            values = {}
            for name in ("hGenEventCount", "hGenEventSumw"):
                h = handle.Get(name)
                if not h or not h.InheritsFrom("TH1") or h.GetNbinsX() != 1:
                    raise ValueError("missing_or_invalid_" + name)
                value = float(h.GetBinContent(1))
                if not math.isfinite(value):
                    raise ValueError("nonfinite_" + name)
                values[name] = value
            if values["hGenEventCount"] <= 0 or not values["hGenEventCount"].is_integer():
                raise ValueError("invalid_genEventCount")
            # Signed sums may be negative or zero for an individual split job.
            result.update(genEventCount=int(values["hGenEventCount"]), genEventSumw=values["hGenEventSumw"])
        if expected is not None and input_events != expected:
            raise ValueError("processed_input_count_differs_from_DAS_assigned_files")
        # Verified full assigned-file counts take precedence over stale logs.
        if expected is None and partial_attempt(latest, input_events):
            raise ValueError("assigned_input_loaded_no_entries_in_failed_attempt")
        if expected is None and latest and latest["loaded_inputs"] and latest["input_events_in_log"] == input_events:
            if set(latest["loaded_inputs"]) != set(job["inputs"]):
                raise ValueError("logged_input_files_do_not_match_assigned_files")
        if expected is None and latest and set(latest["loaded_inputs"]) == set(job["inputs"]):
            expected = latest["input_events_in_log"]
            if expected is not None and expected != input_events:
                raise ValueError("output_input_count_differs_from_complete_input_log")
        result["status"] = "passed"
    except Exception as error:
        result["reason"] = str(error)
    finally:
        if handle:
            handle.Close()
    return key, result


def summaries(manifest, records):
    result = {}
    groups = defaultdict(list)
    for key, job in manifest["jobs"].items():
        groups[job["sample_key"]].append(records[key])
    for name, sample in manifest["samples"].items():
        jobs = groups[name]
        valid = [j for j in jobs if j["status"] == "passed"]
        processed = sum(j["input_events"] for j in valid)
        complete = len(valid) == sample["expected_jobs"]
        equal = processed == sample["expected_input_events"]
        total_sumw = math.fsum(j["genEventSumw"] for j in valid) if sample["is_mc"] else None
        result[name] = {"expected_jobs": sample["expected_jobs"], "passed_jobs": len(valid),
            "status": "complete" if complete and equal else "needs_review" if complete else "incomplete",
            "expected_input_events": sample["expected_input_events"], "validated_input_events": processed,
            "event_difference": sample["expected_input_events"] - processed,
            "validated_selected_events": sum(j["selected_events"] for j in valid),
            "validated_genEventCount": sum(j["genEventCount"] for j in valid) if sample["is_mc"] else None,
            "validated_genEventSumw": total_sumw,
            "normalization_ready": complete and equal and (not sample["is_mc"] or total_sumw != 0)}
    return result


def condor_path(text):
    # These submit commands take literal path values, not quoted ClassAd
    # strings. Quoting initialdir makes Condor look for a directory with quotes.
    if re.search(r'[\s",]', text):
        raise ValueError("Unsupported character in Condor path")
    return text


def prepare_retries(round_dir, failed, manifest, args):
    save(round_dir / "failed_jobs.json", [{"job": key, **manifest["jobs"][key]} for key in failed])
    if not failed:
        return None
    submission = args.submission_dir.resolve()
    proxy = args.proxy or os.environ.get("X509_USER_PROXY")
    if not proxy:
        try:
            proxy = subprocess.check_output(["voms-proxy-info", "--path"], text=True, timeout=5).strip()
        except (OSError, subprocess.SubprocessError):
            raise ValueError("Cannot locate proxy for JDL; use --proxy")
    lines = ["Universe = vanilla", "Executable = " + condor_path(str(submission / "runMakeSkims.sh")),
        "initialdir = " + condor_path(str(submission)), "should_transfer_files = YES",
        "when_to_transfer_output = ON_EXIT", 'transfer_output_files = ""',
        "transfer_input_files = " + ", ".join(condor_path(str(submission / n)) for n in
            ("Skim_NanoAOD.tar.gz", "runMakeSkims.sh")),
        "x509userproxy = " + condor_path(proxy), f"request_cpus = {args.cpus}",
        f"request_memory = {args.memory_mb}"]
    for name, extension in (("Output", "stdout"), ("Error", "stderr"), ("Log", "condor")):
        lines.append(name + " = " + condor_path(str(round_dir / "logs" / f"log_$(Cluster)_$(Process).{extension}")))
    for key in failed:
        j = manifest["jobs"][key]
        out = j["output"].rsplit("/", 1)[0]
        out = "/" + urlsplit(out).path.lstrip("/") if out.startswith("root://") else out
        values = [j["year"], j["sample"], str(j["number"]), str(j["total"]), out]
        if any(re.search(r"[^A-Za-z0-9_./:-]", value) for value in values):
            raise ValueError("Unsupported job argument")
        lines.extend(["", "# " + key, "Arguments = " + " ".join(values), "Queue 1"])
    jdl = round_dir / "resubmitJobs.jdl"
    jdl.write_text("\n".join(lines) + "\n")
    (round_dir / "submit.sh").write_text("#!/usr/bin/env bash\nset -e\ncondor_submit " + shlex.quote(str(jdl)) + "\n")
    return str(jdl)


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--submission-dir", type=Path, default=HERE / "tmpSub")
    parser.add_argument("--production", help="Saved-state name; defaults to a manifest fingerprint")
    parser.add_argument("--output-base", help="Override archived output base; local paths also work")
    parser.add_argument("--log-dir", type=Path, action="append", default=[])
    parser.add_argument("--years", nargs="+", choices=YEARS, default=list(YEARS))
    parser.add_argument("--samples", nargs="+")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--io-timeout", type=int, default=30)
    parser.add_argument("--max-jobs", type=int, help="Check at most this many unresolved jobs in this round")
    parser.add_argument("--recheck-all", action="store_true")
    parser.add_argument("--queue-json", type=Path, help="Use an explicit condor_q JSON snapshot")
    parser.add_argument("--input-event-counts", type=Path,
                        help="Cache per-input DAS counts from JSON {'files': {'/store/...root': N}}")
    parser.add_argument("--proxy")
    parser.add_argument("--cpus", type=int, default=4)
    parser.add_argument("--memory-mb", type=int, default=9216)
    parser.add_argument("--plan", action="store_true", help="Inspect configuration/logs without EOS, queue queries or writes")
    args = parser.parse_args(argv)
    for name in ("workers", "io_timeout", "cpus", "memory_mb"):
        if getattr(args, name) < 1:
            parser.error(name + " must be positive")
    if args.max_jobs is not None and args.max_jobs < 1:
        parser.error("--max-jobs must be positive")
    if args.production and (args.production in (".", "..") or not re.fullmatch(r"[A-Za-z0-9_.-]+", args.production)):
        parser.error("Invalid production name")
    return args


def main(argv=None):
    args = arguments(argv)
    manifest = manifest_for(args)
    name = args.production or "production_" + manifest["fingerprint"][:12]
    state_dir = args.submission_dir.resolve() / "checks" / name
    log_dirs = [args.submission_dir / "log", args.submission_dir / "log_resub", *args.log_dir]
    log_dirs.extend(state_dir.glob("round_*/logs"))
    cache_path = state_dir / "log_index.json"
    log_cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    if args.plan:
        attempts, _ = attempts_for(log_dirs, manifest["jobs"], log_cache)
        print(json.dumps({"jobs": len(manifest["jobs"]), "samples": len(manifest["samples"]),
            "jobs_with_logs": len(attempts), "attempts": sum(map(len, attempts.values())),
            "state_directory": str(state_dir), "provenance": manifest["provenance"]}, indent=2))
        return 0
    state_dir.mkdir(parents=True, exist_ok=True)
    with (state_dir / ".lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError("Another checker is using this production state")
        manifest_path, state_path = state_dir / "manifest.json", state_dir / "check_state.json"
        if manifest_path.exists():
            if json.loads(manifest_path.read_text())["fingerprint"] != manifest["fingerprint"]:
                raise ValueError("Production inputs/package changed; use a new --production name")
        else:
            save(manifest_path, dict(manifest, created_utc=now()))
        state = json.loads(state_path.read_text()) if state_path.exists() else {
            "schema_version": SCHEMA, "fingerprint": manifest["fingerprint"], "created_utc": now(),
            "round": 0, "jobs": {k: {"status": "unchecked"} for k in manifest["jobs"]}}
        if state["fingerprint"] != manifest["fingerprint"] or set(state["jobs"]) != set(manifest["jobs"]):
            raise ValueError("State does not match manifest")
        counts = input_count_cache(state_dir, args.input_event_counts)
        expected_counts = {key: sum(counts["files"][p] for p in job["inputs"])
                           for key, job in manifest["jobs"].items()
                           if all(p in counts["files"] for p in job["inputs"])}
        state["input_count_cache"] = {"path": str(state_dir / "input_event_counts.json"),
                                     "jobs_covered": len(expected_counts), "sources": counts["sources"]}
        attempts, log_cache = attempts_for(log_dirs, manifest["jobs"], log_cache)
        save(cache_path, log_cache)
        number = state["round"] + 1
        while (state_dir / f"round_{number:03d}").exists():
            number += 1
        round_dir = state_dir / f"round_{number:03d}"
        (round_dir / "logs").mkdir(parents=True)
        state["round"] = number
        state["last_round"] = str(round_dir)
        active, queue_error = queue_snapshot(args, manifest["jobs"])
        inventory = inventories(manifest, args.io_timeout)  # Listing failure must never mean all jobs failed.
        def latest_changed(key, record):
            previous = record.get("attempts", [])
            current = attempts.get(key, [])
            return bool(current and (not previous or any(current[-1].get(field) != previous[-1].get(field)
                        for field in ("stdout", "mtime_ns", "error_lines"))))
        targets = [k for k, r in state["jobs"].items() if args.recheck_all or r["status"] != "passed"
                   or latest_changed(k, r)
                   or (k in expected_counts and r.get("expected_input_events") != expected_counts[k])
                   or k in active or manifest["jobs"][k]["filename"] not in inventory[manifest["jobs"][k]["year"]]
                   or (k not in expected_counts and partial_attempt(attempts[k][-1] if attempts.get(k) else None, r.get("input_events")))]
        if args.max_jobs:
            targets = targets[:args.max_jobs]
        print(f"Round {number}: {len(targets)} jobs to check; {len(state['jobs'])-len(targets)} cached/unselected; {args.workers} workers", flush=True)
        tasks, checked = [], []
        for key in targets:
            job = manifest["jobs"][key]
            record = state["jobs"][key]
            record.pop("queue", None)
            record.update(attempts=attempts.get(key, []), last_round=number)
            if key in active:
                record.update(status="pending", reason="condor_" + active[key]["status"], queue=active[key], checked_utc=now())
                checked.append(key)
            elif job["filename"] not in inventory[job["year"]]:
                record.update(status="unknown" if queue_error else "failed",
                    reason="missing_output_queue_unavailable" if queue_error else "missing_output", checked_utc=now())
                checked.append(key)
            else:
                history = record["attempts"]
                record.update(status="checking", reason=None)
                tasks.append((key, dict(job, expected_input_events=expected_counts.get(key)), history[-1] if history else None))
        def checkpoint():
            state["updated_utc"] = now()
            state["queue_error"] = queue_error
            state["sample_summaries"] = summaries(manifest, state["jobs"])
            if queue_error:
                for summary in state["sample_summaries"].values():
                    summary["normalization_ready"] = False
            save(state_path, state)
        checkpoint()
        try:
            if tasks:
                import importlib.util
                if importlib.util.find_spec("ROOT") is None:
                    raise RuntimeError("Initialize the CMS/ROOT environment before checking ROOT files")
                with mp.get_context("spawn").Pool(args.workers, init_worker, (args.io_timeout,)) as pool:
                    last_save = time.monotonic()
                    for key, result in pool.imap_unordered(root_check, tasks, chunksize=1):
                        state["jobs"][key].update(result)
                        checked.append(key)
                        if len(checked) % 25 == 0 or time.monotonic() - last_save > 5:
                            if time.monotonic() - last_save > 5:
                                checkpoint()
                                last_save = time.monotonic()
                            print(f"Checked {len(checked)}/{len(targets)} in this round", flush=True)
        finally:
            checkpoint()
        # No duplicate retries when a queue query was unavailable.
        failed = sorted(k for k in checked if state["jobs"][k]["status"] == "failed") if not queue_error else []
        jdl = prepare_retries(round_dir, failed, manifest, args)
        statuses = dict(Counter(r["status"] for r in state["jobs"].values()))
        report = {"schema_version": SCHEMA, "round": number, "finished_utc": now(),
            "checked_this_round": len(checked), "root_files_checked": len(tasks), "statuses": statuses,
            "queue_error": queue_error, "resubmission_jdl": jdl, "retry_jobs": failed,
            "sample_summaries": state["sample_summaries"], "state_file": str(state_path),
            "normalization_export": "Not produced here; requires separate finalization against EOS/DAS"}
        save(round_dir / "report.json", report)
        print(json.dumps({k: v for k, v in report.items() if k != "sample_summaries"}, indent=2), flush=True)
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (Exception, KeyboardInterrupt) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        sys.exit(2)
