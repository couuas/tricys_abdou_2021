#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""TRICYS V&V: Individual Figure Configuration Runner & Review Test Harness.

Allows reviewing, validating, and testing each figure's YAML configuration in v&v/configs/
one by one or in a batch.

Usage:
    # Run and test all 18 figure configs:
    python "v&v/scripts/test_figure_configs.py"

    # Run and test a single specific figure config:
    python "v&v/scripts/test_figure_configs.py" --config Fig04_tbr_vs_burnup.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

import yaml

# Add repo root and VV_DIR to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
VV_DIR = SCRIPT_DIR.parent
REPO_ROOT = VV_DIR.parent if (VV_DIR.parent / "tricys").exists() else VV_DIR
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(VV_DIR))

from tricys.utils.config_utils import basic_prepare_config
from tricys.workflow.cli_helper import compile_v2_cli
from tricys.workflow.context import PipelineContext
from tricys.workflow.registry import PluginRegistry
import plugins.abdou_plugins  # ensure all plugins registered on-demand from v&v

CONFIGS_DIR = VV_DIR / "configs"
FIGURES_DIR = VV_DIR / "figures"


def run_single_config(config_file: Path) -> bool:
    """Validates, compiles, and executes postprocessing for a single figure config."""
    print(f"\n{'='*75}")
    print(f"🔬 Testing Figure Config: {config_file.name}")
    print(f"{'='*75}")

    # 1. Syntax & Schema Validation
    try:
        raw_cfg, _ = basic_prepare_config(str(config_file))
        task_type = raw_cfg.get("task", {}).get("type", "unknown")
        print(f"  [1/3] ✅ Schema 2.0 Validation: PASS (Task: {task_type.upper()})")
    except Exception as e:
        print(f"  [1/3] ❌ Schema 2.0 Validation FAILED: {e}")
        return False

    # 2. Pipeline DAG Compilation
    try:
        dag = compile_v2_cli(str(config_file))
        print(f"  [2/3] ✅ Pipeline DAG Compilation: PASS")
    except Exception as e:
        print(f"  [2/3] ❌ Pipeline DAG Compilation FAILED: {e}")
        return False

    # 3. Postprocess Plugin Execution
    plugins_cfg = raw_cfg.get("plugins", {}).get("postprocess", [])
    if not plugins_cfg:
        print(f"  [3/3] ⚠️ No postprocessing plugins mounted.")
        return True

    success = True
    for p_entry in plugins_cfg:
        p_name = p_entry.get("name")
        p_params = p_entry.get("params", {})
        p_cls = PluginRegistry.get_postprocess_class(p_name)
        if not p_cls:
            print(f"  [3/3] ❌ Plugin '{p_name}' not found in PluginRegistry!")
            return False

        try:
            plugin_inst = p_cls(**p_params)
            ctx = PipelineContext(
                config=raw_cfg,
                results_dir=str(VV_DIR),
            )
            plugin_inst.run(ctx)
            target_fig = FIGURES_DIR / f"{config_file.stem}.png"
            if target_fig.exists():
                size_kb = target_fig.stat().st_size / 1024.0
                print(f"  [3/3] ✅ Plugin Execution: PASS -> Output: {target_fig.name} ({size_kb:.1f} KB)")
            else:
                print(f"  [3/3] ✅ Plugin Execution: PASS -> Generated artifacts: {list(ctx.artifacts.keys())}")
        except Exception as e:
            print(f"  [3/3] ❌ Plugin '{p_name}' execution FAILED: {e}")
            success = False

    return success


def main():
    parser = argparse.ArgumentParser(description="Test and review Abdou 2021 individual figure configs.")
    parser.add_argument("--config", "-c", type=str, default="", help="Specific YAML config file name to test (e.g. Fig04_tbr_vs_burnup.yaml)")
    args = parser.parse_args()

    if args.config:
        p = Path(args.config)
        if p.is_absolute():
            target_path = p
        elif (REPO_ROOT / p).exists():
            target_path = REPO_ROOT / p
        elif (CONFIGS_DIR / p).exists():
            target_path = CONFIGS_DIR / p
        elif (CONFIGS_DIR / "track1" / p).exists():
            target_path = CONFIGS_DIR / "track1" / p
        elif (CONFIGS_DIR / "track2" / p).exists():
            target_path = CONFIGS_DIR / "track2" / p
        else:
            target_path = CONFIGS_DIR / p

        if not target_path.exists():
            print(f"❌ Configuration file not found: {target_path}")
            sys.exit(1)
        configs_to_run = [target_path]
    else:
        configs_to_run = sorted(list(CONFIGS_DIR.glob("**/*.yaml")))

    print("=" * 75)
    print(f"📋 TRICYS V&V: Reviewing & Testing {len(configs_to_run)} Figure Configurations")
    print("=" * 75)

    results = {}
    for c in configs_to_run:
        ok = run_single_config(c)
        results[c.name] = ok

    print("\n" + "=" * 75)
    print("📊 V&V CONFIGURATION REVIEW & EXECUTION SUMMARY MATRIX")
    print("=" * 75)
    for cname, ok in results.items():
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"  {status}  |  {cname}")

    all_ok = all(results.values())
    if all_ok:
        print(f"\n🎉 100% of figure configurations ({len(results)}/{len(results)}) passed review & execution!")
        sys.exit(0)
    else:
        print(f"\n⚠️ Some configurations failed execution.")
        sys.exit(1)


if __name__ == "__main__":
    main()
