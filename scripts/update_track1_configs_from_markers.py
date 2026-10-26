#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate and update all 11 YAML configurations in v&v/configs/track1/

Strictly aligned with the literature discrete calculation markers in
v&v/Abdou2021/Discrete_Calculation_Markers/.
"""

from pathlib import Path
import yaml
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TRACK1_DIR = REPO_ROOT / "v&v" / "configs" / "track1"
MARKERS_DIR = REPO_ROOT / "v&v" / "Abdou2021" / "Discrete_Calculation_Markers"

STANDARD_HEADER = {
    "version": "2.0",
    "model": {
        "fileName": "../../models/Abdou2021.mo",
        "modelName": "Abdou2021.Cycle",
    },
    "scenario": {
        "time_base": "hour",
        "startTime": 0.0,
        "stopTime": 50000.0,
        "stepSize": 1.0,
        "method": "dassl",
        "tolerance": 1e-4,
        "variableFilter": "time|comp11_Storage.inventory|plant_total_inv|plant_mass_residual",
    },
}

OPTIMIZATION_TRACK1_DEFAULT = {
    "track": "track1_basis",
    "track1": {
        "mode": "direct",
    },
    "outer": {
        "target_metric": {
            "source": "comp11_Storage.inventory",
            "evaluate": "min_value",
            "comparator": ">=",
        }
    },
    "inner": {
        "metric_name": "Required_TBR",
        "parameter": "Lambda",
        "target_metric": {
            "source": "comp11_Storage.inventory",
            "evaluate": "doubling_time",
            "threshold": 43830.0,
            "comparator": "<=",
        },
    },
}

def calc_param_case(P_fus, AF, prod_pct, t_r, q_fail, t_d, tau_9, f_DIR, case_name):
    prod = prod_pct / 100.0
    eta_f = 0.25
    f_b = round(prod / eta_f, 6)
    N_dot_nom = 19.125 * (P_fus / 3000.0)
    I_reserve = round((N_dot_nom / prod) * t_r * q_fail, 4)
    c = {
        "name": case_name,
        "P_fus": float(P_fus),
        "AF": float(AF),
        "f_b": float(f_b),
        "eta_f": float(eta_f),
        "t_r": float(t_r),
        "q_fail": float(q_fail),
        "comp9_ISS.tau_9": float(tau_9),
        "I_reserve_req": float(I_reserve),
        "f_DIR": float(f_DIR),
    }
    if t_d is not None:
        c["t_d"] = float(t_d)
    return c


# ==============================================================================
# Fig04: Required TBR vs Core Product (27 markers)
# ==============================================================================
def make_fig04():
    df = pd.read_csv(MARKERS_DIR / "Fig04_literature_markers.csv")
    params = []
    tau_map = {1.0: 0.5, 4.0: 3.5, 12.0: 11.5}
    for _, row in df.iterrows():
        tp = float(row["tp_hours"])
        prod_pct = float(row["eta_f_fb_nominal_pct"])
        name = f"Prod_{prod_pct}pct_tp{int(tp)}h"
        params.append(calc_param_case(
            P_fus=3000.0, AF=0.5, prod_pct=prod_pct, t_r=24.0, q_fail=0.25,
            t_d=43830.0, tau_9=tau_map[tp], f_DIR=0.0, case_name=name
        ))
    cfg = dict(STANDARD_HEADER)
    cfg["scenario"]["stopTime"] = 50000.0
    cfg["task"] = {
        "type": "sweep",
        "parallel": True,
        "max_workers": 8,
        "parameters": params,
        "optimization": OPTIMIZATION_TRACK1_DEFAULT,
    }
    cfg["plugins"] = {
        "postprocess": [{"name": "abdou_fig04_tbr_vs_burnup", "params": {"dpi": 300}}]
    }
    return cfg


# ==============================================================================
# Fig05: Required TBR vs Availability Factor (22 markers + 6 Table 5 inset)
# ==============================================================================
def make_fig05():
    df = pd.read_csv(MARKERS_DIR / "Fig05_literature_markers.csv")
    params = []
    # Inset: Table 5 ITER reference points
    for af_pct in [10.0, 30.0, 50.0, 70.0, 90.0, 100.0]:
        af = af_pct / 100.0
        c = {
            "name": f"Table5_AF{int(af_pct)}pct_prod0.09pct",
            "AF": float(af),
            "P_fus": 3000.0,
            "f_b": 0.0036,
            "eta_f": 0.25,
            "t_r": 24.0,
            "q_fail": 0.25,
            "t_d": 43830.0,
            "comp9_ISS.tau_9": 3.5,
            "I_reserve_req": 127500.0,
            "f_DIR": 0.0,
        }
        params.append(c)

    # Main 22 markers
    for _, row in df.iterrows():
        prod_pct = float(row["eta_f_fb_pct"])
        af_pct = float(row["AF_nominal_pct"])
        af = round(af_pct / 100.0, 4)
        name = f"Prod{prod_pct}pct_AF{af_pct}pct"
        params.append(calc_param_case(
            P_fus=3000.0, AF=af, prod_pct=prod_pct, t_r=24.0, q_fail=0.25,
            t_d=43830.0, tau_9=3.5, f_DIR=0.0, case_name=name
        ))

    cfg = dict(STANDARD_HEADER)
    cfg["scenario"]["stopTime"] = 50000.0
    cfg["task"] = {
        "type": "sweep",
        "parallel": True,
        "max_workers": 8,
        "parameters": params,
        "optimization": OPTIMIZATION_TRACK1_DEFAULT,
    }
    cfg["plugins"] = {
        "postprocess": [{"name": "abdou_fig05_tbr_vs_availability", "params": {"dpi": 300}}]
    }
    return cfg


# ==============================================================================
# Fig06: Required TBR vs DIR Bypass (20 markers)
# ==============================================================================
def make_fig06():
    df = pd.read_csv(MARKERS_DIR / "Fig06_literature_markers.csv")
    params = []
    for _, row in df.iterrows():
        prod_pct = float(row["eta_f_fb_pct"])
        dir_pct = float(row["DIR_nominal_pct"])
        f_dir = round(dir_pct / 100.0, 2)
        name = f"Prod{prod_pct}pct_DIR{int(dir_pct)}pct"
        params.append(calc_param_case(
            P_fus=3000.0, AF=0.5, prod_pct=prod_pct, t_r=24.0, q_fail=0.25,
            t_d=43830.0, tau_9=3.5, f_DIR=f_dir, case_name=name
        ))

    cfg = dict(STANDARD_HEADER)
    cfg["scenario"]["stopTime"] = 50000.0
    cfg["task"] = {
        "type": "sweep",
        "parallel": True,
        "max_workers": 8,
        "parameters": params,
        "optimization": OPTIMIZATION_TRACK1_DEFAULT,
    }
    cfg["plugins"] = {
        "postprocess": [{"name": "abdou_fig06_tbr_vs_dir", "params": {"dpi": 300}}]
    }
    return cfg


# ==============================================================================
# Fig07: Near-Term FNSF TBR vs Doubling Time (AF=30%, tp=4h, 9 core product points)
# ==============================================================================
def make_fig07():
    df = pd.read_csv(MARKERS_DIR / "Fig07_literature_markers.csv")
    prods = sorted(df["eta_f_fb_nominal_pct"].unique())
    params = []
    for prod_pct in prods:
        name = f"Prod_{prod_pct}pct_AF30pct"
        params.append(calc_param_case(
            P_fus=3000.0, AF=0.3, prod_pct=prod_pct, t_r=24.0, q_fail=0.25,
            t_d=None, tau_9=3.5, f_DIR=0.0, case_name=name
        ))

    opt = dict(OPTIMIZATION_TRACK1_DEFAULT)
    opt["inner"] = dict(OPTIMIZATION_TRACK1_DEFAULT["inner"])
    opt["inner"]["target_metric"] = {
        "source": "comp11_Storage.inventory",
        "evaluate": "doubling_time",
        "threshold": [8766.0, 26298.0, 43830.0, 61362.0],
        "comparator": "<=",
    }

    cfg = dict(STANDARD_HEADER)
    cfg["scenario"]["stopTime"] = 70000.0
    cfg["task"] = {
        "type": "sweep",
        "parallel": True,
        "max_workers": 8,
        "parameters": params,
        "optimization": opt,
    }
    cfg["plugins"] = {
        "postprocess": [{"name": "abdou_fig07_tbr_vs_doubling_time_4h", "params": {"dpi": 300}}]
    }
    return cfg


# ==============================================================================
# Fig08: Commercial DEMO TBR vs Doubling Time (AF=80%, tp=1h, 9 core product points)
# ==============================================================================
def make_fig08():
    df = pd.read_csv(MARKERS_DIR / "Fig08_literature_markers.csv")
    prods = sorted(df["eta_f_fb_nominal_pct"].unique())
    params = []
    for prod_pct in prods:
        name = f"Prod_{prod_pct}pct_AF80pct"
        # Figure 8 is Commercial 1h, so tau_9 is 0.5 h!
        params.append(calc_param_case(
            P_fus=3000.0, AF=0.8, prod_pct=prod_pct, t_r=24.0, q_fail=0.25,
            t_d=None, tau_9=0.5, f_DIR=0.0, case_name=name
        ))

    opt = dict(OPTIMIZATION_TRACK1_DEFAULT)
    opt["inner"] = dict(OPTIMIZATION_TRACK1_DEFAULT["inner"])
    opt["inner"]["target_metric"] = {
        "source": "comp11_Storage.inventory",
        "evaluate": "doubling_time",
        "threshold": [8766.0, 26298.0, 43830.0, 61362.0],
        "comparator": "<=",
    }

    cfg = dict(STANDARD_HEADER)
    cfg["scenario"]["stopTime"] = 70000.0
    cfg["task"] = {
        "type": "sweep",
        "parallel": True,
        "max_workers": 8,
        "parameters": params,
        "optimization": opt,
    }
    cfg["plugins"] = {
        "postprocess": [{"name": "abdou_fig08_tbr_vs_doubling_time_1h", "params": {"dpi": 300}}]
    }
    return cfg


# ==============================================================================
# Fig10: Start-up Inventory Collapse vs Core Product (24 markers)
# ==============================================================================
def make_fig10():
    df = pd.read_csv(MARKERS_DIR / "Fig10_literature_markers.csv")
    params = []
    tau_map = {1.0: 0.5, 4.0: 3.5, 12.0: 11.5}
    for _, row in df.iterrows():
        tp = float(row["tp_hours"])
        prod_pct = float(row["eta_f_fb_nominal_pct"])
        name = f"Prod{prod_pct}pct_tp{int(tp)}h"
        params.append(calc_param_case(
            P_fus=3000.0, AF=1.0, prod_pct=prod_pct, t_r=24.0, q_fail=0.25,
            t_d=43830.0, tau_9=tau_map[tp], f_DIR=0.0, case_name=name
        ))

    cfg = dict(STANDARD_HEADER)
    cfg["scenario"]["stopTime"] = 50000.0
    cfg["task"] = {
        "type": "sweep",
        "parallel": True,
        "max_workers": 8,
        "parameters": params,
        "optimization": OPTIMIZATION_TRACK1_DEFAULT,
    }
    cfg["plugins"] = {
        "postprocess": [{"name": "abdou_fig10_startup_inventory_vs_burnup", "params": {"dpi": 300}}]
    }
    return cfg


# ==============================================================================
# Fig11: Start-up Inventory vs DIR Bypass (20 markers)
# ==============================================================================
def make_fig11():
    df = pd.read_csv(MARKERS_DIR / "Fig11_literature_markers.csv")
    params = []
    for _, row in df.iterrows():
        prod_pct = float(row["eta_f_fb_pct"])
        dir_pct = float(row["DIR_nominal_pct"])
        f_dir = round(dir_pct / 100.0, 2)
        name = f"Prod{prod_pct}pct_DIR{int(dir_pct)}pct"
        params.append(calc_param_case(
            P_fus=3000.0, AF=1.0, prod_pct=prod_pct, t_r=24.0, q_fail=0.25,
            t_d=43830.0, tau_9=3.5, f_DIR=f_dir, case_name=name
        ))

    cfg = dict(STANDARD_HEADER)
    cfg["scenario"]["stopTime"] = 50000.0
    cfg["task"] = {
        "type": "sweep",
        "parallel": True,
        "max_workers": 8,
        "parameters": params,
        "optimization": OPTIMIZATION_TRACK1_DEFAULT,
    }
    cfg["plugins"] = {
        "postprocess": [{"name": "abdou_fig11_startup_inventory_vs_dir", "params": {"dpi": 300}}]
    }
    return cfg


# ==============================================================================
# Fig12: Start-up Inventory vs Reserve Time (30 markers)
# ==============================================================================
def make_fig12():
    df = pd.read_csv(MARKERS_DIR / "Fig12_literature_markers.csv")
    params = []
    for _, row in df.iterrows():
        prod_pct = float(row["eta_f_fb_pct"])
        tr = float(row["reserve_time_tr_hours"])
        tr_label = int(tr) if tr.is_integer() else tr
        name = f"Prod{prod_pct}pct_tr{tr_label}h"
        params.append(calc_param_case(
            P_fus=3000.0, AF=1.0, prod_pct=prod_pct, t_r=tr, q_fail=0.25,
            t_d=43830.0, tau_9=3.5, f_DIR=0.0, case_name=name
        ))

    cfg = dict(STANDARD_HEADER)
    cfg["scenario"]["stopTime"] = 50000.0
    cfg["task"] = {
        "type": "sweep",
        "parallel": True,
        "max_workers": 8,
        "parameters": params,
        "optimization": OPTIMIZATION_TRACK1_DEFAULT,
    }
    cfg["plugins"] = {
        "postprocess": [{"name": "abdou_fig12_startup_inventory_vs_reserve_time", "params": {"dpi": 300}}]
    }
    return cfg


# ==============================================================================
# Fig13: Reserve Inventory vs Reserve Time (30 markers, Algebraic)
# ==============================================================================
def make_fig13():
    df = pd.read_csv(MARKERS_DIR / "Fig13_literature_markers.csv")
    params = []
    for _, row in df.iterrows():
        prod_pct = float(row["eta_f_fb_pct"])
        tr = float(row["reserve_time_tr_hours"])
        tr_label = int(tr) if tr.is_integer() else tr
        name = f"Prod{prod_pct}pct_tr{tr_label}h"
        params.append(calc_param_case(
            P_fus=3000.0, AF=1.0, prod_pct=prod_pct, t_r=tr, q_fail=0.25,
            t_d=43830.0, tau_9=3.5, f_DIR=0.0, case_name=name
        ))

    cfg = dict(STANDARD_HEADER)
    cfg["scenario"]["stopTime"] = 50000.0
    cfg["task"] = {
        "type": "sweep",
        "parallel": True,
        "max_workers": 8,
        "parameters": params,
    }
    cfg["plugins"] = {
        "postprocess": [{"name": "abdou_fig13_reserve_inventory_vs_reserve_time", "params": {"dpi": 300}}]
    }
    return cfg


# ==============================================================================
# Fig14: Required TBR vs Reserve Time (30 markers)
# ==============================================================================
def make_fig14():
    df = pd.read_csv(MARKERS_DIR / "Fig14_literature_markers.csv")
    params = []
    for _, row in df.iterrows():
        prod_pct = float(row["eta_f_fb_pct"])
        tr = float(row["reserve_time_tr_hours"])
        tr_label = int(tr) if tr.is_integer() else tr
        name = f"Prod{prod_pct}pct_tr{tr_label}h"
        params.append(calc_param_case(
            P_fus=3000.0, AF=0.5, prod_pct=prod_pct, t_r=tr, q_fail=0.25,
            t_d=43830.0, tau_9=3.5, f_DIR=0.0, case_name=name
        ))

    cfg = dict(STANDARD_HEADER)
    cfg["scenario"]["stopTime"] = 50000.0
    cfg["task"] = {
        "type": "sweep",
        "parallel": True,
        "max_workers": 8,
        "parameters": params,
        "optimization": OPTIMIZATION_TRACK1_DEFAULT,
    }
    cfg["plugins"] = {
        "postprocess": [{"name": "abdou_fig14_tbr_vs_reserve_time", "params": {"dpi": 300}}]
    }
    return cfg


# ==============================================================================
# Fig15: Start-up Inventory vs Fusion Power (28 markers)
# ==============================================================================
def make_fig15():
    df = pd.read_csv(MARKERS_DIR / "Fig15_literature_markers.csv")
    params = []
    for _, row in df.iterrows():
        prod_pct = float(row["eta_f_fb_pct"])
        tr = float(row["reserve_time_tr_hours"])
        pfus = float(row["fusion_power_MW"])
        name = f"P{int(pfus)}MW_prod{prod_pct}pct_tr{int(tr)}h"
        params.append(calc_param_case(
            P_fus=pfus, AF=1.0, prod_pct=prod_pct, t_r=tr, q_fail=0.25,
            t_d=43830.0, tau_9=3.5, f_DIR=0.0, case_name=name
        ))

    cfg = dict(STANDARD_HEADER)
    cfg["scenario"]["stopTime"] = 50000.0
    cfg["task"] = {
        "type": "sweep",
        "parallel": True,
        "max_workers": 8,
        "parameters": params,
        "optimization": OPTIMIZATION_TRACK1_DEFAULT,
    }
    cfg["plugins"] = {
        "postprocess": [{"name": "abdou_fig15_startup_inventory_vs_power", "params": {"dpi": 300}}]
    }
    return cfg


CONFIG_GENERATORS = {
    "Fig04_tbr_vs_burnup.yaml": make_fig04,
    "Fig05_tbr_vs_availability.yaml": make_fig05,
    "Fig06_tbr_vs_dir.yaml": make_fig06,
    "Fig07_tbr_vs_doubling_time_4h.yaml": make_fig07,
    "Fig08_tbr_vs_doubling_time_1h.yaml": make_fig08,
    "Fig10_startup_inventory_vs_burnup.yaml": make_fig10,
    "Fig11_startup_inventory_vs_dir.yaml": make_fig11,
    "Fig12_startup_inventory_vs_reserve_time.yaml": make_fig12,
    "Fig13_reserve_inventory_vs_reserve_time.yaml": make_fig13,
    "Fig14_tbr_vs_reserve_time.yaml": make_fig14,
    "Fig15_startup_inventory_vs_power.yaml": make_fig15,
}

def main():
    print("=" * 70)
    print("Updating all Track 1 figure configs to strictly match literature markers...")
    print("=" * 70)

    for fname, gen in CONFIG_GENERATORS.items():
        cfg_data = gen()
        target_path = TRACK1_DIR / fname
        with open(target_path, "w", encoding="utf-8") as f:
            yaml.dump(cfg_data, f, sort_keys=False, indent=2)
        n_cases = len(cfg_data["task"]["parameters"])
        print(f"✅ Updated {fname:<36} ({n_cases} scan cases)")

    print("\nAll 11 Track 1 configurations have been synchronized successfully!")

if __name__ == "__main__":
    main()
