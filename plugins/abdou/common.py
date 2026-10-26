"""Abdou 2021 Benchmark: Common utilities, data loaders, and physical constants.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd

from tricys.workflow.context import PipelineContext

logger = logging.getLogger(__name__)

# Universal physical and engineering constants (Abdou 2021)
HOURS_PER_DAY = 24.0
YEARS_TO_HOURS = 365.25 * HOURS_PER_DAY
TRITIUM_HALF_LIFE_YEARS = 12.32
LAMBDA_PER_HOUR = np.log(2.0) / (TRITIUM_HALF_LIFE_YEARS * YEARS_TO_HOURS)  # 6.425e-6 /h


def get_burn_rate_g_per_h(P_fus_MW: float = 3000.0) -> float:
    """Tritium burning rate in g/h: 3000 MW -> 0.459 kg/day = 19.125 g/h."""
    return (0.459 * 1000.0 * (1.0 / HOURS_PER_DAY)) * (P_fus_MW / 3000.0)


def load_benchmark_data(
    context: PipelineContext,
    figure_key: str,
    candidate_filenames: List[str],
) -> pd.DataFrame:
    """Strict benchmark data loader.

    Resolution hierarchy:
    1. If context contains an in-memory optimization or simulation artifact, use it.
    2. Check context.results_dir for candidates (including required_tbr_summary.csv).
    3. Check candidate filenames in context.results_dir / 'data'.
    4. Fall back to repository verified baseline: v&v/data/<candidate>.
    5. If all fail, raise FileNotFoundError. NO synthetic/empirical data fallback allowed.
    """
    search_dirs: List[Path] = []
    if context.results_dir:
        res_p = Path(context.results_dir)
        search_dirs.extend([res_p, res_p / "data"])

    # 1. First check candidate files in context results_dir
    for cand in candidate_filenames:
        for sdir in search_dirs:
            p = sdir / cand
            if p.exists() and p.is_file():
                try:
                    df = pd.read_csv(p)
                    if not df.empty:
                        logger.info(f"[{figure_key}] Loaded benchmark data from results dir: {p.resolve()}")
                        return df
                except Exception as e:
                    logger.warning(f"Failed to read {p}: {e}")

    # 2. Check runtime sweep_results.h5 in context results directory
    if context.results_dir:
        h5_path = Path(context.results_dir) / "sweep_results.h5"
        if h5_path.exists() and h5_path.is_file():
            try:
                # If timeseries figure (Figs 1, 2, 3), extract raw_df_1 trajectory
                if any(k in figure_key.lower() for k in ["fig01", "fig02", "fig03", "group1", "inventory_evolution", "starvation_valley"]):
                    for key in ["raw_df_1", "raw_df_2", "raw_df_3"]:
                        try:
                            df_raw = pd.read_hdf(h5_path, key)
                            if not df_raw.empty:
                                if "time" in df_raw.columns:
                                    df_raw["time_h"] = df_raw["time"] / 3600.0
                                    df_raw["time_d"] = df_raw["time"] / 86400.0
                                name_map = {
                                    "comp11_Storage.inventory": "sds.inventory",
                                    "comp1_BZ.inventory": "bz.inventory",
                                    "comp2_TES.inventory": "tes.inventory",
                                    "comp8_FCU.inventory": "tep.inventory",
                                    "comp9_ISS.inventory": "i_iss.inventory",
                                    "comp7_Pump.inventory": "ps.inventory",
                                    "comp6_CPS.inventory": "cps_pfc.inventory",
                                    "comp10_EDS_WDS.inventory": "wds.inventory",
                                    "comp3_FW.inventory": "fw.inventory",
                                    "comp4_DIV.inventory": "div.inventory",
                                    "plant_total_inv": "plant_total_inv",
                                }
                                for k, v in name_map.items():
                                    if k in df_raw.columns and v not in df_raw.columns:
                                        df_raw[v] = df_raw[k]
                                logger.info(f"[{figure_key}] Loaded timeseries trajectory from {h5_path} ({key})")
                                return df_raw
                        except Exception:
                            continue
                else:
                    # If sweep figure, extract jobs table
                    try:
                        df_tab = pd.read_hdf(h5_path, "jobs")
                        if not df_tab.empty:
                            logger.info(f"[{figure_key}] Loaded sweep table from {h5_path} ('jobs')")
                            return df_tab
                    except Exception:
                        pass
            except Exception as e:
                logger.warning(f"Failed to inspect sweep_results.h5: {e}")

    # 3. Check required_tbr_summary.csv in results directory
    if context.results_dir:
        for cand in ["required_tbr_summary.csv", "optimization_summary.csv"]:
            p = Path(context.results_dir) / cand
            if p.exists() and p.is_file():
                try:
                    df = pd.read_csv(p)
                    if not df.empty:
                        logger.info(f"[{figure_key}] Loaded summary from results dir: {p.resolve()}")
                        return df
                except Exception:
                    pass

    # 4. Fall back to verified baseline in v&v/data
    vv_data = Path(__file__).resolve().parent.parent.parent / "data"
    for cand in candidate_filenames:
        for p in [vv_data / cand, vv_data / "track2" / cand, vv_data / "track1" / cand]:
            if p.exists() and p.is_file():
                try:
                    df = pd.read_csv(p)
                    if not df.empty:
                        logger.info(f"[{figure_key}] Loaded verified benchmark data from v&v/data: {p.resolve()}")
                        return df
                except Exception as e:
                    logger.warning(f"Failed to read {p}: {e}")

    raise FileNotFoundError(
        f"[{figure_key}] No genuine benchmark data found in candidates {candidate_filenames} "
        f"or results directory {context.results_dir}. Synthetic empirical fallback is strictly disabled."
    )
