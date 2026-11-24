#!/usr/bin/env python3
"""Verify completed skim outputs and export full-sample normalization metadata.

Reads ROOT headers/histograms, never scans events or submits jobs. Failed
validation creates a diagnostic report, never a usable normalization export.
"""
import argparse
from copy import copy
from concurrent.futures import ThreadPoolExecutor
import fcntl
import json
import math
import multiprocessing as mp
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

import checkJobStatus as checker

sys.dont_write_bytecode = True
SKIM = Path(__file__).resolve().parents[1]


def dataset_for(filename):
    parts = checker.canonical(filename).strip("/").split("/")
    if len(parts) < 8 or parts[:2] not in (["store", "mc"], ["store", "data"]):
        raise ValueError("Cannot infer a DAS dataset for " + filename + "; provide --das-counts")
    return f"/{parts[3]}/{parts[2]}-{parts[5]}/{parts[4]}"


def file_counts(records):
    values = {}
    for row in records:
        for entry in row.get("file", []):
            name, count = entry.get("name"), entry.get("nevents")
            if not name or isinstance(count, bool) or not isinstance(count, int) or count < 0:
                raise ValueError("DAS returned a missing/invalid filename or nevents")
            name = checker.canonical(name)
            if name in values and values[name] != count:
                raise ValueError("Conflicting DAS counts for " + name)
            values[name] = count
    return values


def das_metadata(inputs, args, report_dir):
    if args.das_counts:
        raw = args.das_counts.read_bytes()
        source = json.loads(raw)
        values = {}
        for name, count in source["files"].items():
            if isinstance(count, bool) or not isinstance(count, int) or count < 0:
                raise ValueError("Invalid provided DAS count: " + name)
            name = checker.canonical(name)
            if name in values and values[name] != count:
                raise ValueError("Conflicting provided DAS count: " + name)
            values[name] = count
        return values, {"mode": "provided_snapshot", "path": str(args.das_counts.resolve()),
                        "sha256": checker.digest(raw)}, {}
    datasets = sorted({dataset_for(name) for name in inputs})
    def query(dataset):
        result = subprocess.run(["dasgoclient", "--query", "file dataset=" + dataset + " status=valid", "--json"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=args.das_timeout, check=True)
        counts = file_counts(json.loads(result.stdout))
        if not counts:
            raise ValueError("DAS returned no files for " + dataset)
        return dataset, counts
    merged, by_dataset = {}, {}
    with ThreadPoolExecutor(max_workers=min(args.workers, 4)) as pool:
        for index, (dataset, values) in enumerate(pool.map(query, datasets), 1):
            for name, value in values.items():
                if name in merged and merged[name] != value:
                    raise ValueError("Conflicting DAS counts: " + name)
                merged[name] = value
            by_dataset[dataset] = values
            print(f"DAS metadata: {index}/{len(datasets)} datasets", flush=True)
    checker.save(report_dir / "das_counts.json", {"schema_version": 1, "queried_utc": checker.now(),
                                                "datasets": datasets, "files": merged})
    return merged, {"mode": "live_DAS", "queried_utc": checker.now(), "datasets": datasets}, by_dataset


def selected_manifest(manifest, args):
    jobs = {key: value for key, value in manifest["jobs"].items()
            if (not args.years or value["year"] in args.years)
            and (not args.samples or value["sample"] in args.samples)}
    if not jobs:
        raise ValueError("No samples match the requested scope")
    if args.samples and set(args.samples) - {j["sample"] for j in jobs.values()}:
        raise ValueError("Some requested samples are absent from the production")
    samples = {name: manifest["samples"][name] for name in {j["sample_key"] for j in jobs.values()}}
    return dict(manifest, jobs=jobs, samples=samples)


def finalize_one(args):
    directory = args.production_dir.resolve()
    with (directory / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest_bytes = (directory / "manifest.json").read_bytes()
        state_bytes = (directory / "check_state.json").read_bytes()
        manifest, state = json.loads(manifest_bytes), json.loads(state_bytes)
        core = {key: manifest[key] for key in ("schema_version", "provenance", "samples", "jobs")}
        if checker.digest(json.dumps(core, sort_keys=True).encode()) != manifest["fingerprint"]:
            raise ValueError("Manifest fingerprint is invalid")
        if state["fingerprint"] != manifest["fingerprint"]:
            raise ValueError("Checker state does not match manifest")
        scope = selected_manifest(manifest, args)
        scoped = len(scope["jobs"]) != len(manifest["jobs"])
        suffix = "_" + checker.digest(json.dumps(sorted(scope["samples"])).encode())[:8] if scoped else ""
        output = args.output or SKIM / "normalization" / (directory.name + suffix + ".json")
        output = output.resolve()
        if output.suffix != ".json":
            raise ValueError("Normalization output must end in .json")
        root = directory / "finalization"
        root.mkdir(exist_ok=True)
        number = 1
        while (root / f"round_{number:03d}").exists():
            number += 1
        report_dir = root / f"round_{number:03d}"
        report_dir.mkdir()
        report = {"schema_version": 1, "status": "blocked", "normalization_ready": False,
                  "created_utc": checker.now(), "issues": [], "output": str(output),
                  "manifest_fingerprint": manifest["fingerprint"], "jobs": {}, "samples": {}}
        def issue(code, **detail):
            report["issues"].append(dict(code=code, **detail))
        def finish():
            report["finished_utc"] = checker.now()
            checker.save(report_dir / "report.json", report)
            print(json.dumps({"status": report["status"], "issues": report["issues"],
                "normalization_json": str(output) if report["normalization_ready"] else None,
                "report": str(report_dir / "report.json")}, indent=2), flush=True)
            return 0 if report["normalization_ready"] else 2
        try:
            if output.exists():
                issue("output_already_exists", message="Choose another --output filename; existing exports are not overwritten")
            for name, sample in scope["samples"].items():
                members = [j for j in scope["jobs"].values() if j["sample_key"] == name]
                if len(members) != sample["expected_jobs"] or {j["number"] for j in members} != set(range(1, sample["expected_jobs"] + 1)):
                    issue("incomplete_sample_job_manifest", sample=name)
                inputs = [p for j in members for p in j["inputs"]]
                if len(inputs) != len(set(inputs)):
                    issue("duplicate_input_assignment", sample=name)
            outputs = [checker.canonical(j["output"]) for j in scope["jobs"].values()]
            if len(outputs) != len(set(outputs)):
                issue("duplicate_output_assignment")
            for key in scope["jobs"]:
                status = state["jobs"].get(key, {}).get("status", "missing")
                if status != "passed":
                    issue("job_not_passed", job=key, status=status)
            archive = Path(manifest["provenance"]["archive"])
            for path, field in [(archive, "archive_sha256"), (archive.parent / "runMakeSkims.sh", "wrapper_sha256")]:
                if not path.is_file() or checker.digest(path.read_bytes()) != manifest["provenance"][field]:
                    issue("submission_package_changed_or_missing", path=str(path))
            if report["issues"]:
                return finish()
            active, queue_error = checker.queue_snapshot(args, scope["jobs"])
            if queue_error:
                issue("queue_status_unavailable", error=queue_error)
            for key, value in active.items():
                issue("job_still_active", job=key, status=value["status"])
            if report["issues"]:
                return finish()
            all_inputs = {p for job in scope["jobs"].values() for p in job["inputs"]}
            counts, das_source, by_dataset = das_metadata(all_inputs, args, report_dir)
            report["das_source"] = das_source
            for filename in sorted(all_inputs - set(counts)):
                issue("input_missing_from_DAS_counts", input=filename)
            if report["issues"]:
                return finish()
            inventory = checker.inventories(scope, args.io_timeout)
            tasks = []
            for key, job in scope["jobs"].items():
                expected = sum(counts[p] for p in job["inputs"])
                if job["filename"] not in inventory[job["year"]]:
                    issue("missing_EOS_output", job=key)
                else:
                    tasks.append((key, dict(job, expected_input_events=expected), None))
            if report["issues"]:
                return finish()
            print(f"Rereading {len(tasks)} ROOT outputs with {args.workers} worker(s); no event loops", flush=True)
            import importlib.util
            if importlib.util.find_spec("ROOT") is None:
                raise RuntimeError("Initialize the CMS/ROOT environment before checking ROOT files")
            with mp.get_context("spawn").Pool(args.workers, checker.init_worker, (args.io_timeout,)) as pool:
                for index, (key, result) in enumerate(pool.imap_unordered(checker.root_check, tasks, chunksize=1), 1):
                    report["jobs"][key] = result
                    if result["status"] != "passed":
                        issue("EOS_output_validation_failed", job=key, reason=result["reason"])
                    else:
                        for field in ("input_events", "filtered_events", "selected_events", "genEventCount", "genEventSumw"):
                            if field in state["jobs"][key] and state["jobs"][key][field] != result[field]:
                                issue("output_changed_since_check", job=key, field=field)
                    if index % 25 == 0:
                        print(f"ROOT metadata: {index}/{len(tasks)} files", flush=True)
            exported = {}
            for name, sample in sorted(scope["samples"].items()):
                keys = [k for k, j in scope["jobs"].items() if j["sample_key"] == name]
                records = [report["jobs"][k] for k in keys]
                if any(r["status"] != "passed" for r in records):
                    continue
                inputs = {p for key in keys for p in scope["jobs"][key]["inputs"]}
                expected = sum(counts[p] for p in inputs)
                processed = sum(r["input_events"] for r in records)
                if expected != sample["expected_input_events"]:
                    issue("DAS_total_differs_from_submitted_expectation", sample=name,
                          submitted=sample["expected_input_events"], verified_DAS=expected)
                if by_dataset:
                    dataset_files = {p for d in {dataset_for(p) for p in inputs} for p in by_dataset[d]}
                    if dataset_files != inputs:
                        issue("DAS_file_coverage_differs_from_submission", sample=name,
                              additional_DAS_files=len(dataset_files-inputs), missing_DAS_files=len(inputs-dataset_files))
                gen_count = sum(r["genEventCount"] for r in records) if sample["is_mc"] else None
                gen_sumw = math.fsum(r["genEventSumw"] for r in records) if sample["is_mc"] else None
                if sample["is_mc"] and (not math.isfinite(gen_sumw) or abs(gen_sumw) < 1e-12):
                    issue("invalid_full_sample_generator_sum", sample=name, genEventSumw=gen_sumw)
                value = {"is_mc": sample["is_mc"], "expected_jobs": sample["expected_jobs"],
                    "validated_jobs": len(keys), "input_file_count": len(inputs), "das_events": expected,
                    "processed_events": processed, "selected_events": sum(r["selected_events"] for r in records),
                    "genEventCount": gen_count, "genEventSumw": gen_sumw,
                    "normalization_method": "generator_sumw" if sample["is_mc"] else "unit_weight",
                    "files": [scope["jobs"][k]["output"] for k in keys]}
                report["samples"][name] = value
                exported.setdefault(sample["year"], {})[sample["sample"]] = value
            if report["issues"]:
                return finish()
            document = {"schema_version": 1, "status": "complete", "normalization_ready": True,
                "created_utc": checker.now(), "production": directory.name,
                "manifest_fingerprint": manifest["fingerprint"], "state_sha256": checker.digest(state_bytes),
                "provenance": manifest["provenance"], "das_source": das_source,
                "scope": {"full_production": not scoped, "samples": sorted(scope["samples"])},
                "MC_event_normalization": "cross_section_pb * luminosity_pb_inverse * Generator_weight / genEventSumw",
                "samples": exported, "validation_report": str(report_dir / "report.json")}
            document.update(retry_provenance(directory, scope))
            # Output is created only here, after all checks. Never overwrite an export.
            if output.exists():
                issue("output_appeared_during_validation")
                return finish()
            checker.save(output, document)
            report.update(status="complete", normalization_ready=True)
            return finish()
        except Exception as error:
            issue("validation_error", error=str(error))
            return finish()


def retry_provenance(directory, scope):
    """Retain documented retry packages and access-only replica overrides."""
    records = {}
    patterns = {"retry_package_patches": "round_*/patch_record.json",
                "retry_replica_overrides": "round_*/*/replica_override.json"}
    for field, pattern in patterns.items():
        for path in sorted(directory.glob(pattern)):
            raw = path.read_bytes()
            data = json.loads(raw)
            jobs = data.get("retry_jobs", [data.get("job")])
            selected = sorted(set(jobs) & set(scope["jobs"]))
            if not selected:
                continue
            item = dict(data, record_path=str(path), record_sha256=checker.digest(raw), affected_jobs=selected)
            records.setdefault(field, []).append(item)
    return records


def load_production(directory):
    manifest_raw = (directory / "manifest.json").read_bytes()
    state_raw = (directory / "check_state.json").read_bytes()
    manifest, state = json.loads(manifest_raw), json.loads(state_raw)
    core = {k: manifest[k] for k in ("schema_version", "provenance", "samples", "jobs")}
    if checker.digest(json.dumps(core, sort_keys=True).encode()) != manifest["fingerprint"]:
        raise ValueError("Invalid manifest fingerprint: " + str(directory))
    if state["fingerprint"] != manifest["fingerprint"] or set(state["jobs"]) != set(manifest["jobs"]):
        raise ValueError("Checker state does not match manifest: " + str(directory))
    return manifest


def archived_samples(manifest, year):
    path = Path(manifest["provenance"]["archive"])
    if checker.digest(path.read_bytes()) != manifest["provenance"]["archive_sha256"]:
        raise ValueError("Submission package changed: " + str(path))
    with tarfile.open(path, "r:gz") as archive:
        matches = [m for m in archive.getmembers() if m.isfile() and m.name.endswith("/sample/JobsNano_cff.py")]
        if len(matches) != 1:
            raise ValueError("Expected one archived job catalog: " + str(path))
        catalog = checker.literals(archive.extractfile(matches[0]).read().decode())
    return set(catalog.get("Samples_" + year, {}))


def production_plan(args):
    directories = args.production_dir or [p.parent for p in
        args.search_dir.glob("*/checks/*/manifest.json")]
    directories = sorted({p.resolve() for p in directories})
    if not directories:
        raise ValueError("No production records found; provide --production-dir or --search-dir")
    loaded = [(path, load_production(path)) for path in directories]
    years = args.years or [year for year in checker.YEARS
                          if any(j["year"] == year for _, m in loaded for j in m["jobs"].values())]
    sources, owners, expected = [], {}, {year: set() for year in years}
    outputs = set()
    for directory, manifest in loaded:
        jobs = {key: j for key, j in manifest["jobs"].items() if j["year"] in years
                and (not args.samples or j["sample"] in args.samples)}
        if not jobs:
            continue
        sample_keys = {j["sample_key"] for j in jobs.values()}
        for name in sample_keys:
            if name in owners:
                raise ValueError("Overlapping production records for " + name + ": " + str(owners[name]) +
                                 " and " + str(directory) + "; choose --production-dir explicitly")
            owners[name] = directory
        for j in jobs.values():
            output = checker.canonical(j["output"])
            if output in outputs:
                raise ValueError("Duplicate skim output across production records: " + output)
            outputs.add(output)
        local_years = [year for year in years if any(j["year"] == year for j in jobs.values())]
        for year in local_years:
            expected[year].update(archived_samples(manifest, year))
        scope = dict(manifest, jobs=jobs, samples={k: manifest["samples"][k] for k in sample_keys})
        sources.append((directory, scope, local_years))
    if not sources:
        raise ValueError("No production records match the selected years/samples")
    found_names = {j["sample"] for _, scope, _ in sources for j in scope["jobs"].values()}
    if args.samples and set(args.samples) - found_names:
        raise ValueError("Requested samples are absent: " + ", ".join(sorted(set(args.samples) - found_names)))
    for year in years:
        found = {j["sample"] for _, scope, _ in sources for j in scope["jobs"].values() if j["year"] == year}
        wanted = expected[year] & set(args.samples) if args.samples else expected[year]
        if not found or wanted != found:
            raise ValueError("Incomplete production coverage for " + year + "; missing samples: " +
                             ", ".join(sorted(wanted - found)))
    sources.sort(key=lambda item: (min(years.index(year) for year in item[2]), str(item[0])))
    stem = "Run2" if set(years) == set(checker.YEARS) else "_".join(years)
    suffix = "_" + checker.digest(json.dumps(sorted(owners)).encode())[:8] if args.samples else ""
    output = (args.output or SKIM / "normalization" / (stem + "_normalization" + suffix + ".json")).resolve()
    if output.suffix != ".json":
        raise ValueError("Normalization output must end in .json")
    return years, sources, output


def finalize_years(args):
    years, sources, output = production_plan(args)
    preview = {"years": years, "normalization_json": str(output), "existing_output": output.exists(),
               "sources": [{"production_dir": str(path), "years": selected,
                            "samples": len(scope["samples"]), "jobs": len(scope["jobs"])}
                           for path, scope, selected in sources]}
    if args.plan:
        print(json.dumps(preview, indent=2))
        return 0
    if output.exists():
        raise ValueError("Normalization output already exists; choose another --output: " + str(output))
    output.parent.mkdir(parents=True, exist_ok=True)
    report_root = output.parent / "reports"
    report_root.mkdir(exist_ok=True)
    report_dir = Path(tempfile.mkdtemp(prefix=output.stem + "_", dir=report_root))
    report = dict(preview, status="blocked", normalization_ready=False, created_utc=checker.now(), issues=[])
    def finish():
        report["finished_utc"] = checker.now()
        checker.save(report_dir / "report.json", report)
        print(json.dumps({"status": report["status"], "issues": report["issues"],
                          "normalization_json": str(output) if report["normalization_ready"] else None,
                          "report": str(report_dir / "report.json")}, indent=2), flush=True)
        return 0 if report["normalization_ready"] else 2
    try:
        exports, sample_keys, files = [], [], set()
        combined = {}
        all_jobs = {}
        for index, (directory, scope, selected) in enumerate(sources, 1):
            local = copy(args)
            local.production_dir = directory
            local.years = selected
            local.samples = sorted({j["sample"] for j in scope["jobs"].values()}) if args.samples else None
            local.output = report_dir / f"source_{index:03d}.json"
            print(f"Validating production {index}/{len(sources)}: {directory}", flush=True)
            if finalize_one(local):
                report["issues"].append({"code": "source_production_failed", "production_dir": str(directory)})
                return finish()
            raw = local.output.read_bytes()
            document = json.loads(raw)
            all_jobs.update(scope["jobs"])
            if document["status"] != "complete" or not document["normalization_ready"]:
                raise ValueError("Source finalization did not pass")
            expected_keys = set(scope["samples"])
            actual_keys = {year + "/" + name for year, values in document["samples"].items() for name in values}
            if expected_keys != actual_keys:
                raise ValueError("Source export has different sample coverage from the plan")
            for year, values in document["samples"].items():
                for name, value in values.items():
                    canonical = {checker.canonical(p) for p in value["files"]}
                    if (value["validated_jobs"] != value["expected_jobs"] or len(canonical) != value["expected_jobs"]
                            or value["processed_events"] != value["das_events"] or canonical & files):
                        raise ValueError("Incomplete or duplicate source sample: " + year + "/" + name)
                    files.update(canonical)
                    combined.setdefault(year, {})[name] = value
            sample_keys.extend(actual_keys)
            exports.append(dict(path=str(local.output), sha256=checker.digest(raw), production_dir=str(directory),
                                **{k: v for k, v in document.items() if k not in
                                   ("samples", "scope", "status", "normalization_ready", "schema_version")}))
        # A new checker round or submission during validation invalidates this export.
        for item in exports:
            state = Path(item["production_dir"]) / "check_state.json"
            if checker.digest(state.read_bytes()) != item["state_sha256"]:
                raise ValueError("Checker state changed during finalization: " + str(state))
        active, error = checker.queue_snapshot(args, all_jobs)
        if error or active:
            raise ValueError("Queue status changed or is unavailable before export: " + str(error or active))
        counts = {year: len(combined[year]) for year in years}
        document = {"schema_version": 1, "status": "complete", "normalization_ready": True,
                    "created_utc": checker.now(), "production": "Run2_skims" if len(years) == 4 else "_".join(years),
                    "scope": {"full_production": not bool(args.samples),
                              "full_run2": set(years) == set(checker.YEARS) and not args.samples,
                              "years": years, "samples": sorted(sample_keys)},
                    "summary": {"samples_per_year": counts, "total_samples": len(sample_keys),
                                "validated_skim_files": len(files)},
                    "MC_event_normalization": exports[0]["MC_event_normalization"],
                    "source_productions": exports, "samples": combined,
                    "validation_report": str(report_dir / "report.json")}
        if output.exists():
            raise ValueError("Output appeared during validation; existing export is preserved")
        checker.save(output, document)
        report.update(status="complete", normalization_ready=True, summary=document["summary"])
        return finish()
    except Exception as error:
        report["issues"].append({"code": "validation_error", "error": str(error)})
        return finish()


def finalize(args):
    # Preserve the original CLI, default filename and report layout when no
    # year-selection or discovery feature is requested.
    if args.production_dir and len(args.production_dir) == 1 and args.years is None and not args.plan:
        local = copy(args)
        local.production_dir = args.production_dir[0]
        return finalize_one(local)
    return finalize_years(args)


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--production-dir", type=Path, action="append",
                        help="Explicit production record; repeat for multiple productions")
    parser.add_argument("--search-dir", type=Path, default=SKIM / "condor",
                        help="Discover */checks/* production records below this directory")
    parser.add_argument("--plan", action="store_true", help="Preview year/source/output coverage without EOS/DAS access or writes")
    parser.add_argument("--output", type=Path, help="Override the JSON path; default: normalization/<years>_normalization.json")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--io-timeout", type=int, default=30)
    parser.add_argument("--das-timeout", type=int, default=180)
    parser.add_argument("--das-counts", type=Path, help="Explicit DAS per-file snapshot instead of live DAS queries")
    parser.add_argument("--queue-json", type=Path, help="Explicit Condor queue snapshot; normal use queries the live queue")
    parser.add_argument("--years", nargs="+", choices=(*checker.YEARS, "all"))
    parser.add_argument("--samples", nargs="+", help="Export only complete named samples; scope is recorded")
    args = parser.parse_args(argv)
    if min(args.workers, args.io_timeout, args.das_timeout) < 1:
        parser.error("Worker count and timeouts must be positive")
    if not args.production_dir and not args.years:
        parser.error("provide --years or --production-dir")
    if args.years:
        if len(args.years) != len(set(args.years)) or ("all" in args.years and args.years != ["all"]):
            parser.error("use distinct years, or --years all by itself")
        args.years = list(checker.YEARS) if args.years == ["all"] else [y for y in checker.YEARS if y in args.years]
    return args


if __name__ == "__main__":
    try:
        sys.exit(finalize(arguments()))
    except (Exception, KeyboardInterrupt) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        sys.exit(2)
