#!/usr/bin/env python3
"""Run a selected skim or a checker's failed_jobs.json locally; never submit Condor jobs."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tarfile
import threading

from condor import checkJobStatus as checker

HERE = Path(__file__).resolve().parent


def positive(text):
    if not re.fullmatch(r"[1-9][0-9]*", str(text)):
        raise argparse.ArgumentTypeError("must be a positive integer")
    return int(text)


def arguments(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("selection", nargs="*", metavar="YEAR SAMPLE [JOB TOTAL]")
    p.add_argument("--failed-jobs", type=Path, help="Retry list written by checkJobStatus.py")
    p.add_argument("--years", nargs="+", choices=checker.YEARS, help="Filter the retry list")
    p.add_argument("--samples", nargs="+", help="Filter the retry list")
    p.add_argument("--output-dir", type=Path, help="Default: a new directory under local_runs/")
    p.add_argument("--threads", type=positive, default=os.environ.get("SKIM_THREADS", "4"))
    p.add_argument("--parallel", type=positive, default=os.environ.get("SKIM_MAX_PARALLEL", "1"))
    p.add_argument("--stage-out", action="store_true", help="For retries: copy to the recorded EOS output, then remove the local ROOT copy")
    p.add_argument("--dry-run", action="store_true", help="Validate and print the plan without processing or creating files")
    a = p.parse_args(argv)
    if a.failed_jobs:
        if a.selection:
            p.error("use a direct selection or --failed-jobs, not both")
    elif len(a.selection) not in (2, 4) or a.years or a.samples or a.stage_out:
        p.error("supply YEAR SAMPLE [JOB TOTAL], or --failed-jobs FILE; --stage-out and filters apply only to retries")
    a.output_dir = (a.output_dir or HERE / "local_runs" /
                    (datetime.now().strftime("local_%Y%m%dT%H%M%S_") + str(os.getpid()))).resolve()
    return a


def file_lists(text):
    return dict(re.findall(r'^([A-Za-z_]\w*)="([^"\n]*)"[ \t]*$', text, re.MULTILINE))


def archive_read(archive, suffix):
    members = [m for m in archive.getmembers() if m.isfile() and m.name.endswith("/" + suffix)]
    if len(members) != 1:
        raise ValueError("Archive must contain exactly one " + suffix)
    return archive.extractfile(members[0]).read()


def plan(args):
    manifest, binary = None, None
    if args.failed_jobs:
        source = args.failed_jobs.resolve()
        records = json.loads(source.read_text())
        if not isinstance(records, list):
            raise ValueError("failed_jobs.json must contain a list")
        if not records:
            return [], None, None
        locations = [source.parent / "manifest.json", source.parent.parent / "manifest.json"]
        manifest_path = next((p for p in locations if p.is_file()), None)
        if not manifest_path:
            raise ValueError("Cannot locate the retry list's production manifest")
        manifest = json.loads(manifest_path.read_text())
        core = {k: manifest[k] for k in ("schema_version", "provenance", "samples", "jobs")}
        if checker.digest(json.dumps(core, sort_keys=True).encode()) != manifest["fingerprint"]:
            raise ValueError("Production manifest fingerprint is invalid")
        package = Path(manifest["provenance"]["archive"])
        if checker.digest(package.read_bytes()) != manifest["provenance"]["archive_sha256"]:
            raise ValueError("The frozen submission package changed")
        with tarfile.open(package, "r:gz") as archive:
            lists = file_lists(archive_read(archive, "sample/FilesNano_cff.sh").decode())
            binary = archive_read(archive, "makeSkim")
        jobs, seen = [], set()
        for record in records:
            key = record["job"]
            if key in seen:
                raise ValueError("Duplicate retry job: " + key)
            seen.add(key)
            expected = manifest["jobs"][key]
            if {k: v for k, v in record.items() if k != "job"} != expected:
                raise ValueError("Retry record differs from its production manifest: " + key)
            if args.years and expected["year"] not in args.years:
                continue
            if args.samples and expected["sample"] not in args.samples:
                continue
            jobs.append(dict(expected, job=key))
        if not jobs:
            raise ValueError("No retry jobs match the requested filters")
    else:
        year, sample = args.selection[:2]
        number, total = map(positive, args.selection[2:]) if len(args.selection) == 4 else (1, 1)
        if year not in checker.YEARS or not re.fullmatch(r"[A-Za-z_]\w*", sample):
            raise ValueError("Invalid era or sample name")
        lists = file_lists((HERE / "sample/FilesNano_cff.sh").read_text())
        jobs = [dict(year=year, sample=sample, number=number, total=total,
                     is_mc="Data" not in sample, job=checker.job_key(year, sample, number, total))]
    for job in jobs:
        year, sample, number, total = (job[k] for k in ("year", "sample", "number", "total"))
        tokens = shlex.split(lists[f"{sample}_FileList_{year}"])
        if len(tokens) < 2 or tokens[0] not in ("local", "xrootd"):
            raise ValueError("Invalid file list for " + job["job"])
        if not 1 <= number <= total:
            raise ValueError("Invalid split for " + job["job"])
        if manifest and tokens[0] == "local" and any(not Path(p).is_absolute() and "://" not in p for p in tokens[1:]):
            raise ValueError("Archived local input paths must be absolute")
        if tokens[0] == "local":
            tokens[1:] = [str((HERE / p).resolve()) if "://" not in p else p for p in tokens[1:]]
        canonical = [checker.canonical(p) for p in tokens[1:]]
        if len(set(canonical)) != len(canonical):
            raise ValueError("Duplicate inputs for " + job["job"])
        assigned = checker.split_files(canonical, total)[number - 1]
        if manifest and assigned != job["inputs"]:
            raise ValueError("Archived input splitting differs from the manifest")
        job["input_args"] = tokens
        job["assigned_files"] = len(assigned)
        job["local_base"] = str(args.output_dir / year / (sample + "_Skim.root"))
        job["local_output"] = job["local_base"][:-5] + f"_{number}of{total}.root"
        if Path(job["local_output"]).exists() or Path(job["local_output"]).is_symlink():
            raise ValueError("Refusing to overwrite " + job["local_output"])
        if args.stage_out and not job.get("output", "").startswith("root://"):
            raise ValueError("Stage-out requires a recorded root:// EOS destination")
    return jobs, manifest, binary


def main(argv=None):
    args = arguments(argv)
    jobs, manifest, binary = plan(args)
    if not jobs:
        print("No failed jobs to run.")
        return 0
    print(f"{len(jobs)} job(s); {args.parallel} concurrent; {args.threads} thread(s) per skim")
    print("Output:", args.output_dir)
    for job in jobs:
        print(f"  {job['job']}: {job['assigned_files']} assigned input file(s) -> {job['local_output']}")
    if args.dry_run:
        return 0
    if not shutil.which("root-config"):
        raise ValueError("Initialize the CMS/ROOT environment before running locally")
    if args.stage_out and not shutil.which("xrdcp"):
        raise ValueError("xrdcp is required for --stage-out")
    if args.stage_out:
        active, error = checker.queue_snapshot(argparse.Namespace(queue_json=None, io_timeout=30),
                                               {job["job"]: job for job in jobs})
        if error:
            raise ValueError("Cannot check Condor before EOS stage-out: " + error)
        if active:
            raise ValueError("Selected retry jobs are still active in Condor: " + ", ".join(sorted(active)))
    executable = HERE / "makeSkim"
    if binary is None and not os.access(executable, os.X_OK):
        raise ValueError("Build makeSkim first with make")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if binary is not None:
        saved_manifest = args.output_dir / "manifest.json"
        if saved_manifest.exists() and json.loads(saved_manifest.read_text())["fingerprint"] != manifest["fingerprint"]:
            raise ValueError("Output directory belongs to another production manifest")
        executable = args.output_dir / ".production" / "makeSkim"
        executable.parent.mkdir(exist_ok=True)
        if executable.exists() and executable.read_bytes() != binary:
            raise ValueError("Output directory contains a different frozen executable")
        if not executable.exists():
            executable.write_bytes(binary)
            executable.chmod(0o755)
        checker.save(args.output_dir / "manifest.json", manifest)
    stop, lock, children = threading.Event(), threading.Lock(), set()

    def execute(command, stdout, stderr):
        with lock:
            if stop.is_set():
                return 130
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr, start_new_session=True)
            children.add(process)
        try:
            return process.wait()
        finally:
            with lock:
                children.discard(process)

    def run(job):
        directory = Path(job["local_base"]).parent
        directory.mkdir(exist_ok=True)
        logs = directory / "logs"
        logs.mkdir(exist_ok=True)
        stem = f"{job['sample']}_{job['number']}of{job['total']}"
        result = dict(job=job["job"], status="failed", output=job["local_output"],
                      stdout=str(logs / (stem + ".stdout")), stderr=str(logs / (stem + ".stderr")))
        try:
            with open(result["stdout"], "w") as out, open(result["stderr"], "w") as err:
                command = [str(executable), "--threads", str(args.threads), "--mc" if job["is_mc"] else "--data",
                           job["year"], f"{job['number']}of{job['total']}", job["local_base"], *job["input_args"]]
                result["exit_code"] = execute(command, out, err)
                if result["exit_code"]:
                    return result
                output = Path(job["local_output"])
                if not output.is_file() or output.stat().st_size == 0:
                    raise ValueError("Skimmer returned success without a nonempty output")
                if args.stage_out:
                    result["stage_out_exit_code"] = execute(["xrdcp", "-f", str(output), job["output"]], out, err)
                    if result["stage_out_exit_code"]:
                        return result
                    output.unlink()
                    result["EOS_output"] = job["output"]
                result["status"] = "passed"
        except Exception as error:
            result["reason"] = str(error)
        return result

    results, was_interrupted = [], False
    pool = ThreadPoolExecutor(max_workers=args.parallel)
    try:
        pending = {pool.submit(run, job): job for job in jobs}
        for future in as_completed(pending):
            result = future.result()
            results.append(result)
            print(result["status"].upper() + ": " + result["job"], flush=True)
    except KeyboardInterrupt:
        was_interrupted = True
        stop.set()
        with lock:
            running = list(children)
        for process in running:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        for process in running:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
        print("Interrupted; partial ROOT files and logs remain in", args.output_dir, file=sys.stderr)
        return 130
    finally:
        pool.shutdown(wait=True, cancel_futures=True)
        checker.save(args.output_dir / "run_summary.json", {"finished_utc": checker.now(),
                                                           "interrupted": was_interrupted, "jobs": results})
    failed = {r["job"] for r in results if r["status"] != "passed"}
    if manifest:
        checker.save(args.output_dir / "failed_jobs.json", [dict(manifest["jobs"][key], job=key) for key in sorted(failed)])
    print(f"Finished: {len(results)-len(failed)} passed; {len(failed)} failed.")
    return 1 if failed else 0


def interrupted(signum, frame):
    raise KeyboardInterrupt


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, interrupted)
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, argparse.ArgumentTypeError) as error:
        print("ERROR:", error, file=sys.stderr)
        sys.exit(2)
