"""Resolve the declared Zhang data sources to immutable HF commits and hashes."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
from pathlib import Path
import urllib.parse
import urllib.request


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "source_manifest.json"
DEFAULT_LOCK = HERE / "source_manifest.lock.json"


def _get_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"User-Agent": "agi-evaluation-repro/1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def expand_cells(manifest: dict) -> list[dict]:
    models = manifest["data"]["models"]
    cells: list[dict] = []
    for benchmark in manifest["data"]["benchmarks"]:
        overrides = benchmark.get("suffix_overrides", {})
        for model in models:
            suffix = overrides.get(model["key"], model["suffix"])
            fields = {"prefix": benchmark["repo_prefix"], "suffix": suffix}
            cells.append({
                "cell": f"{benchmark['key']}.{model['key']}",
                "benchmark": benchmark["key"],
                "benchmark_label": benchmark["label"],
                "model": model["key"],
                "model_label": model["label"],
                "baseline_repo": benchmark["baseline_pattern"].format(**fields),
                "perturbed_repo": benchmark["perturbed_pattern"].format(**fields),
            })
    return cells


def resolve_dataset(repo: str) -> tuple[str, dict]:
    encoded_repo = urllib.parse.quote(repo, safe="/")
    metadata = _get_json(f"https://huggingface.co/api/datasets/{encoded_repo}")
    revision = metadata["sha"]
    encoded_revision = urllib.parse.quote(revision, safe="")
    tree = _get_json(
        f"https://huggingface.co/api/datasets/{encoded_repo}/tree/"
        f"{encoded_revision}?recursive=true&expand=true"
    )
    parquet = []
    for entry in tree:
        if entry.get("type") != "file" or not entry["path"].endswith(".parquet"):
            continue
        lfs = entry.get("lfs") or {}
        path = entry["path"]
        parquet.append({
            "path": path,
            "bytes": int(entry.get("size", 0)),
            "git_oid": entry.get("oid"),
            "lfs_sha256": lfs.get("oid"),
            "download_url": (
                f"https://huggingface.co/datasets/{repo}/resolve/{revision}/"
                f"{urllib.parse.quote(path, safe='/')}?download=true"
            ),
        })
    if not parquet:
        raise RuntimeError(f"No Parquet files found for {repo}@{revision}")
    card_data = metadata.get("cardData") or {}
    return repo, {
        "repo": repo,
        "revision": revision,
        "private": bool(metadata.get("private")),
        "gated": metadata.get("gated", False),
        "license": card_data.get("license"),
        "parquet": sorted(parquet, key=lambda item: item["path"]),
    }


def pin(manifest_path: Path, output_path: Path, workers: int = 8) -> dict:
    manifest = json.loads(manifest_path.read_text())
    cells = expand_cells(manifest)
    repos = sorted({cell[key] for cell in cells for key in ("baseline_repo", "perturbed_repo")})
    resolved: dict[str, dict] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(resolve_dataset, repo): repo for repo in repos}
        for future in concurrent.futures.as_completed(futures):
            repo, value = future.result()
            if value["private"] or value["gated"]:
                raise RuntimeError(f"Expected public, ungated dataset: {repo}")
            resolved[repo] = value
    lock = {
        "schema_version": manifest["schema_version"],
        "pinned_on": manifest["pinned_on"],
        "paper": manifest["paper"],
        "code": manifest["code"],
        "cells": cells,
        "datasets": {key: resolved[key] for key in sorted(resolved)},
    }
    output_path.write_text(json.dumps(lock, indent=2, sort_keys=False) + "\n")
    return lock


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    lock = pin(args.manifest, args.output, args.workers)
    print(f"Pinned {len(lock['datasets'])} datasets across {len(lock['cells'])} cells")
    print(args.output)


if __name__ == "__main__":
    main()
