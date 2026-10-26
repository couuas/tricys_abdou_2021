#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate Publication-Quality Comparison & Error Figures: TRICYS Track 1 vs Abdou 2021 Literature Truth.
===========================================================================================================
Generates dual-panel scientific figures (Left: Truth vs Track 1 Comparison; Right: Error Analysis)
for all 11 figures (Fig04, Fig05, Fig06, Fig07, Fig08, Fig10, Fig11, Fig12, Fig13, Fig14, Fig15).

Outputs:
  - Saved to v&v/figures/track1_comparison/
  - Copied to artifact directory for presentation
"""

from __future__ import annotations

import shutil
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
VV_DIR = REPO_ROOT / "v&v"
DETAILED_CSV = VV_DIR / "data" / "track1_vs_literature_error_detailed.csv"
OUT_DIR = VV_DIR / "figures" / "track1_comparison"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Artifact destination for Antigravity presentation
ARTIFACT_DIR = Path(r"C:\Users\Administrator\.gemini\antigravity-ide\brain\f560003c-6919-4414-adf4-b597169487f0")

FIGURE_METADATA = {
    "Fig04": {
        "title": "Figure 4: Required TBR vs Core Product (P_fus = 3 GW, AF = 50%, DIR = 0%)",
        "x_label": r"Core Product $\eta_f f_b$ [%]",
        "y_label": "Required TBR",
        "x_scale": "log",
        "metric_unit": "",
        "curve_names": {
            "tp_1h": r"$t_p = 1\,$h (Advanced)",
            "tp_4h": r"$t_p = 4\,$h (Reference)",
            "tp_12h": r"$t_p = 12\,$h (Conservative)",
        },
    },
    "Fig05": {
        "title": "Figure 5: Required TBR vs Availability AF (P_fus = 3 GW, DIR = 0%, tp = 4 h)",
        "x_label": "Plant Availability Factor AF [%]",
        "y_label": "Required TBR",
        "x_scale": "linear",
        "metric_unit": "",
        "curve_names": {
            "eta_f_fb_0.5pct": r"$\eta_f f_b = 0.5\%$",
            "eta_f_fb_1.0pct": r"$\eta_f f_b = 1.0\%$",
            "eta_f_fb_2.0pct": r"$\eta_f f_b = 2.0\%$",
            "eta_f_fb_3.0pct": r"$\eta_f f_b = 3.0\%$",
        },
    },
    "Fig06": {
        "title": "Figure 6: Required TBR vs Direct Internal Recycling (P_fus = 3 GW, AF = 50%, tp = 4 h)",
        "x_label": r"Direct Internal Recycling $f_{\mathrm{DIR}}$ [%]",
        "y_label": "Required TBR",
        "x_scale": "linear",
        "metric_unit": "",
        "curve_names": {
            "eta_f_fb_0.5pct": r"$\eta_f f_b = 0.5\%$",
            "eta_f_fb_1.0pct": r"$\eta_f f_b = 1.0\%$",
            "eta_f_fb_2.0pct": r"$\eta_f f_b = 2.0\%$",
            "eta_f_fb_3.0pct": r"$\eta_f f_b = 3.0\%$",
        },
    },
    "Fig07": {
        "title": "Figure 7: Required TBR vs Core Product for Doubling Times (Near-Term, AF = 30%, tp = 4 h)",
        "x_label": r"Core Product $\eta_f f_b$ [%]",
        "y_label": "Required TBR",
        "x_scale": "log",
        "metric_unit": "",
        "curve_names": {
            "td_1yr": r"$t_d = 1\,$yr",
            "td_3yr": r"$t_d = 3\,$yr",
            "td_5yr": r"$t_d = 5\,$yr",
            "td_7yr": r"$t_d = 7\,$yr",
        },
    },
    "Fig08": {
        "title": "Figure 8: Required TBR vs Core Product for Doubling Times (Commercial, AF = 80%, tp = 1 h)",
        "x_label": r"Core Product $\eta_f f_b$ [%]",
        "y_label": "Required TBR",
        "x_scale": "log",
        "metric_unit": "",
        "curve_names": {
            "td_1yr": r"$t_d = 1\,$yr",
            "td_3yr": r"$t_d = 3\,$yr",
            "td_5yr": r"$t_d = 7\,$yr",  # Note td_5yr corresponds to td=5yr
            "td_7yr": r"$t_d = 7\,$yr",
        },
    },
    "Fig10": {
        "title": "Figure 10: Startup Inventory vs Core Product (P_fus = 3 GW, AF = 100%, tr = 24 h)",
        "x_label": r"Core Product $\eta_f f_b$ [%]",
        "y_label": "Startup Inventory $I_{S,0}$ [kg]",
        "x_scale": "log",
        "metric_unit": " kg",
        "curve_names": {
            "tp_1h": r"$t_p = 1\,$h",
            "tp_4h": r"$t_p = 4\,$h",
            "tp_12h": r"$t_p = 12\,$h",
        },
    },
    "Fig11": {
        "title": "Figure 11: Startup Inventory vs DIR (P_fus = 3 GW, AF = 100%, tr = 24 h, tp = 4 h)",
        "x_label": r"Direct Internal Recycling $f_{\mathrm{DIR}}$ [%]",
        "y_label": "Startup Inventory $I_{S,0}$ [kg]",
        "x_scale": "linear",
        "metric_unit": " kg",
        "curve_names": {
            "eta_f_fb_0.5pct": r"$\eta_f f_b = 0.5\%$",
            "eta_f_fb_1.0pct": r"$\eta_f f_b = 1.0\%$",
            "eta_f_fb_2.0pct": r"$\eta_f f_b = 2.0\%$",
            "eta_f_fb_3.0pct": r"$\eta_f f_b = 3.0\%$",
        },
    },
    "Fig12": {
        "title": "Figure 12: Startup Inventory vs Reserve Time (P_fus = 3 GW, AF = 100%, DIR = 0%, tp = 4 h)",
        "x_label": r"Reserve Time $t_r$ [hours]",
        "y_label": "Startup Inventory $I_{S,0}$ [kg]",
        "x_scale": "linear",
        "metric_unit": " kg",
        "curve_names": {
            "prod_0.5pct": r"$\eta_f f_b = 0.5\%$",
            "prod_1.0pct": r"$\eta_f f_b = 1.0\%$",
            "prod_2.0pct": r"$\eta_f f_b = 2.0\%$",
            "prod_3.0pct": r"$\eta_f f_b = 3.0\%$",
            "prod_5.0pct": r"$\eta_f f_b = 5.0\%$",
        },
    },
    "Fig13": {
        "title": "Figure 13: Reserve Inventory vs Reserve Time (P_fus = 3 GW, AF = 100%, DIR = 0%, tp = 4 h)",
        "x_label": r"Reserve Time $t_r$ [hours]",
        "y_label": "Reserve Inventory $I_r$ [kg]",
        "x_scale": "linear",
        "metric_unit": " kg",
        "curve_names": {
            "prod_0.5pct": r"$\eta_f f_b = 0.5\%$",
            "prod_1.0pct": r"$\eta_f f_b = 1.0\%$",
            "prod_2.0pct": r"$\eta_f f_b = 2.0\%$",
            "prod_3.0pct": r"$\eta_f f_b = 3.0\%$",
            "prod_5.0pct": r"$\eta_f f_b = 5.0\%$",
        },
    },
    "Fig14": {
        "title": "Figure 14: Required TBR vs Reserve Time (P_fus = 3 GW, AF = 100%, DIR = 0%, tp = 4 h)",
        "x_label": r"Reserve Time $t_r$ [hours]",
        "y_label": "Required TBR",
        "x_scale": "linear",
        "metric_unit": "",
        "curve_names": {
            "prod_0.5pct": r"$\eta_f f_b = 0.5\%$",
            "prod_1.0pct": r"$\eta_f f_b = 1.0\%$",
            "prod_2.0pct": r"$\eta_f f_b = 2.0\%$",
            "prod_3.0pct": r"$\eta_f f_b = 3.0\%$",
            "prod_5.0pct": r"$\eta_f f_b = 5.0\%$",
        },
    },
    "Fig15": {
        "title": "Figure 15: Startup Inventory vs Fusion Power (AF = 100%, DIR = 0%, tp = 4 h)",
        "x_label": r"Fusion Power $P_{\mathrm{fus}}$ [MW]",
        "y_label": "Startup Inventory $I_{S,0}$ [kg]",
        "x_scale": "linear",
        "metric_unit": " kg",
        "curve_names": {
            "prod_0.5pct_tr24h": r"$\eta_f f_b = 0.5\%,\ t_r = 24\,$h",
            "prod_0.5pct_tr6h": r"$\eta_f f_b = 0.5\%,\ t_r = 6\,$h",
            "prod_5.0pct_tr24h": r"$\eta_f f_b = 5.0\%,\ t_r = 24\,$h",
            "prod_5.0pct_tr6h": r"$\eta_f f_b = 5.0\%,\ t_r = 6\,$h",
        },
    },
}

PALETTE = [
    "#1f77b4",  # Steel Blue
    "#d62728",  # Crimson
    "#2ca02c",  # Forest Green
    "#ff7f0e",  # Amber / Dark Orange
    "#9467bd",  # Purple
    "#8c564b",  # Brown
]


def plot_single_figure(fig_key: str, df_fig: pd.DataFrame) -> Path:
    meta = FIGURE_METADATA.get(fig_key, {
        "title": f"{fig_key}: TRICYS Track 1 vs Literature Ground Truth",
        "x_label": "X Parameter",
        "y_label": "Value",
        "x_scale": "linear",
        "metric_unit": "",
        "curve_names": {},
    })

    # Prepare figure with 2 subplots (Left: Comparison, Right: Error Analysis)
    fig, (ax_cmp, ax_err) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    plt.subplots_adjust(wspace=0.28, left=0.07, right=0.95, top=0.88, bottom=0.12)

    curves = df_fig["curve"].unique()
    
    # Track statistics
    mae = df_fig["abs_error"].mean()
    mre = df_fig["rel_error_pct"].mean()
    max_err = df_fig["rel_error_pct"].max()
    max_abs = df_fig["abs_error"].max()

    for idx, curve_id in enumerate(curves):
        color = PALETTE[idx % len(PALETTE)]
        curve_label = meta["curve_names"].get(curve_id, curve_id)
        
        c_df = df_fig[df_fig["curve"] == curve_id].sort_values("x_val")
        x = c_df["x_val"].values
        y_lit = c_df["y_lit"].values
        y_sim = c_df["y_sim"].values
        signed_err = c_df["signed_error"].values
        rel_err = c_df["rel_error_pct"].values

        # Left panel: TRICYS (Line + filled dot) vs Literature (Open square / diamond)
        ax_cmp.plot(
            x, y_sim,
            color=color, linestyle="-", linewidth=2.0, marker="o", markersize=6,
            label=f"{curve_label} (TRICYS Track 1)", alpha=0.9
        )
        ax_cmp.scatter(
            x, y_lit,
            edgecolors=color, facecolors="none", s=70, linewidths=2.2,
            marker="s", label=f"{curve_label} (Abdou 2021 Truth)", zorder=5
        )

        # Right panel: Signed deviation & relative error points
        ax_err.plot(
            x, signed_err,
            color=color, linestyle="--", linewidth=1.5, marker="o", markersize=5.5,
            label=f"{curve_label} Error", alpha=0.85
        )

    # --- Left Panel Styling ---
    ax_cmp.set_title(r"$\bf{(a)}$ Model Trajectory Comparison", fontsize=12, pad=10, loc="left")
    ax_cmp.set_xlabel(meta["x_label"], fontsize=11, fontweight="medium")
    ax_cmp.set_ylabel(meta["y_label"], fontsize=11, fontweight="medium")
    if meta["x_scale"] == "log":
        ax_cmp.set_xscale("log")
    ax_cmp.grid(True, linestyle=":", alpha=0.4, color="gray")
    ax_cmp.spines["top"].set_visible(False)
    ax_cmp.spines["right"].set_visible(False)
    ax_cmp.legend(fontsize=8, loc="best", framealpha=0.85, edgecolor="#cccccc")

    # --- Right Panel Styling ---
    ax_err.set_title(r"$\bf{(b)}$ Absolute Deviation Residual ($\Delta = y_{\mathrm{sim}} - y_{\mathrm{lit}}$)", fontsize=12, pad=10, loc="left")
    ax_err.set_xlabel(meta["x_label"], fontsize=11, fontweight="medium")
    ax_err.set_ylabel(f"Deviation ({meta['y_label'].split('[')[0].strip()}{meta['metric_unit']})", fontsize=11, fontweight="medium")
    if meta["x_scale"] == "log":
        ax_err.set_xscale("log")
    ax_err.axhline(0, color="black", linestyle="-", linewidth=1.0, alpha=0.6)
    ax_err.grid(True, linestyle=":", alpha=0.4, color="gray")
    ax_err.spines["top"].set_visible(False)
    ax_err.spines["right"].set_visible(False)

    # Add Summary Text Box in Error Panel
    unit = meta["metric_unit"]
    stats_text = (
        f"Points: {len(df_fig)}\n"
        f"MAE: {mae:.4f}{unit}\n"
        f"Max Dev: {max_abs:.4f}{unit}\n"
        f"Mean Rel Err: {mre:.2f}%\n"
        f"Max Rel Err: {max_err:.2f}%"
    )
    ax_err.text(
        0.04, 0.96, stats_text,
        transform=ax_err.transAxes,
        fontsize=8.5, verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8f9fa", edgecolor="#b0bec5", alpha=0.92)
    )

    # Overall Suptitle
    fig.suptitle(f"TRICYS Track 1 V&V vs Abdou (2021) Literature Ground Truth — {meta['title']}", fontsize=13, fontweight="bold")

    out_path = OUT_DIR / f"{fig_key}_track1_vs_literature.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Also copy to artifact dir
    artifact_copy = ARTIFACT_DIR / f"{fig_key}_track1_vs_literature.png"
    shutil.copy2(out_path, artifact_copy)

    print(f"✅ Generated: {out_path.name} -> Copied to Artifact Directory")
    return out_path


def main(target_fig: str = None):
    if not DETAILED_CSV.exists():
        raise FileNotFoundError(f"Missing {DETAILED_CSV}")

    df = pd.read_csv(DETAILED_CSV)
    if target_fig:
        figures = [target_fig]
    else:
        figures = sorted(df["figure"].unique())
    print(f"🎨 Generating 2-panel comparison and error plots for {len(figures)} figure(s)...")

    for fig_key in figures:
        df_fig = df[df["figure"] == fig_key]
        if not df_fig.empty:
            plot_single_figure(fig_key, df_fig)

    print(f"\n🎉 {len(figures)} figure(s) successfully generated and synced to both repository and artifact space!")


if __name__ == "__main__":
    import sys
    tgt = sys.argv[1] if len(sys.argv) > 1 else None
    main(tgt)
