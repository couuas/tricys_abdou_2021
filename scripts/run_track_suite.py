#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""TRICYS Track Suite Runner.
==========================
Executes configurations from either v&v/configs/track1/ or v&v/configs/track2/,
synchronizes simulation outputs (CSVs) into v&v/data/{track}/,
and figure outputs (PNGs) into v&v/figures/{track}/.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VV_DIR = REPO_ROOT / "v&v"


def run_single_config(config_path: Path, track: str) -> bool:
    """Executes a single config and syncs artifacts to v&v/data/{track} and v&v/figures/{track}."""
    config_name = config_path.name
    fig_match = re.match(r"(Fig\d+|opt_[a-zA-Z0-9_]+)", config_name)
    prefix = fig_match.group(1) if fig_match else config_path.stem

    data_dest_dir = VV_DIR / "data" / track
    fig_dest_dir = VV_DIR / "figures" / track
    data_dest_dir.mkdir(parents=True, exist_ok=True)
    fig_dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*75}")
    print(f"🚀 Running [{track.upper()}] Config: {config_name}")
    print(f"{'='*75}")

    cmd = [sys.executable, "-m", "tricys", "run", "-c", str(config_path)]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)

    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), env=env)
    if proc.returncode != 0:
        print(f"❌ Execution failed for {config_name}")
        return False

    print(f"✅ Simulation completed for {config_name}")

    # Locate output directory from latest timestamped folder
    candidate_dirs = [REPO_ROOT / "results"]
    timestamp_dirs = sorted(
        [d for d in REPO_ROOT.glob("202*_*") if d.is_dir() and (d / "results").exists()],
        key=os.path.getmtime,
        reverse=True,
    )
    if timestamp_dirs:
        candidate_dirs.insert(0, timestamp_dirs[0] / "results")

    synced_csv = False
    for r_dir in candidate_dirs:
        if not r_dir.exists():
            continue

        # Sync figures
        for fig_f in r_dir.glob("*.png"):
            dest = fig_dest_dir / fig_f.name
            shutil.copy2(fig_f, dest)
            print(f"  📸 Synchronized figure: {dest.name} -> v&v/figures/{track}/")

        # Sync CSV summaries
        summary_csv = r_dir / "required_tbr_summary.csv"
        if summary_csv.exists():
            dest = data_dest_dir / f"{prefix}_required_tbr_summary.csv"
            shutil.copy2(summary_csv, dest)
            # Also maintain canonical required_tbr_summary.csv
            shutil.copy2(summary_csv, data_dest_dir / "required_tbr_summary.csv")
            print(f"  💾 Synchronized summary: {dest.name} -> v&v/data/{track}/")
            synced_csv = True

        for other_csv in r_dir.glob("*.csv"):
            if other_csv.name not in ("required_tbr_summary.csv", "requierd_tbr_summary.csv"):
                dest = data_dest_dir / other_csv.name
                shutil.copy2(other_csv, dest)
                print(f"  💾 Synchronized dataset: {dest.name} -> v&v/data/{track}/")
                synced_csv = True

        if synced_csv:
            break

    # Clean up temporary timestamped run directory to avoid repository clutter
    if timestamp_dirs and timestamp_dirs[0].exists():
        try:
            shutil.rmtree(timestamp_dirs[0], ignore_errors=True)
            print(f"  🧹 Cleaned temporary folder: {timestamp_dirs[0].name}")
        except Exception as e:
            print(f"  ⚠️ Could not clean {timestamp_dirs[0].name}: {e}")

    return True


def run_track(track: str, specific_configs: Optional[List[str]] = None) -> None:
    """Runs all or specified configs for the target track."""
    configs_dir = VV_DIR / "configs" / track
    if not configs_dir.exists():
        raise FileNotFoundError(f"Configs directory not found: {configs_dir}")

    if specific_configs:
        config_files = [configs_dir / c if not c.endswith(".yaml") else configs_dir / c for c in specific_configs]
    else:
        config_files = sorted(configs_dir.glob("Fig*.yaml"))

    print(f"\n=======================================================")
    print(f"  TRICYS TRACK RUNNER: {track.upper()} ({len(config_files)} configurations)")
    print(f"=======================================================")

    success_count = 0
    for cfg in config_files:
        if not cfg.exists():
            print(f"⚠️ Warning: Config file not found: {cfg}")
            continue
        ok = run_single_config(cfg, track)
        if ok:
            success_count += 1

    print(f"\n🏁 Finished {track.upper()} Suite: {success_count}/{len(config_files)} passed.")

    # Automatically trigger literature ground truth error comparison audit
    cmp_script = VV_DIR / "scripts" / "compare_track_with_literature.py"
    if cmp_script.exists():
        print(f"\n=======================================================")
        print(f"  GROUND TRUTH COMPARISON AUDIT ({track.upper()})")
        print(f"=======================================================")
        subprocess.run([sys.executable, str(cmp_script), "--track", track], cwd=str(REPO_ROOT))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run TRICYS track suites (track1 or track2).")
    parser.add_argument("--track", choices=["track1", "track2"], default="track1", help="Target solving track")
    parser.add_argument("--configs", nargs="*", help="Specific config filenames (e.g. Fig04_tbr_vs_burnup.yaml)")
    args = parser.parse_args()

    run_track(args.track, args.configs)
