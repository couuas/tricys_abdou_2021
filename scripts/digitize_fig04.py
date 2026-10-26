#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""High-Fidelity Digitization of Abdou 2021 Figure 04.

Extracts ground truth numerical data for:
- Required TBR vs Core Product (eta_f * f_b in %)
- Three curves: tp = 1 h, tp = 4 h (reference), tp = 12 h
- Fixed parameters: P_fus = 3 GW, AF = 50%, t_r = 24 h, q = 25%, t_d = 5 yr, f_DIR = 0

Outputs:
1. v&v/data/track2/Fig04_literature_digitized.csv (Discrete marker benchmark table)
2. v&v/data/track2/Fig04_literature_dense_curves.csv (Dense continuous curves, dx=0.01%)
3. v&v/data/track2/Fig04_literature_digitized.yaml (YAML benchmark schema)
4. v&v/data/track2/Fig04_literature_comparison.csv (Side-by-side comparison with TRICYS solver)
5. v&v/Abdou2021/Fig04_digitization_overlay.png (Visual verification overlay)
6. v&v/figures/comparison/Fig04_digitization_verification.png (Multi-panel V&V audit plot)
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import scipy.interpolate
import scipy.ndimage
import matplotlib.pyplot as plt
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
IMAGE_PATH = REPO_ROOT / "v&v" / "Abdou2021" / "Fig04.png"
OUTPUT_DIR = REPO_ROOT / "v&v" / "data" / "track2"
FIG_DIR = REPO_ROOT / "v&v" / "figures" / "comparison"
SIM_CSV = OUTPUT_DIR / "Fig04_required_tbr_summary.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Coordinate System Calibration
# -----------------------------------------------------------------------------
# Axis lines detected via sub-pixel profile analysis on 1973 x 1570 image
X_LEFT_PX = 225.0       # eta_f * f_b = 0.0%
X_RIGHT_PX = 1955.0     # eta_f * f_b = 5.0%
X_SPAN_PX = X_RIGHT_PX - X_LEFT_PX  # 1730.0 px
DX_PER_UNIT = X_SPAN_PX / 5.0       # 346.0 px / %

Y_TOP_PX = 17.0         # TBR = 1.30
Y_BOTTOM_PX = 1386.0    # TBR = 1.00
Y_SPAN_PX = Y_BOTTOM_PX - Y_TOP_PX  # 1369.0 px
# Linear fit from 7 ticks: [1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30] -> [1386, 1159, 932, 702, 475, 248, 17]
Y_SLOPE = -4562.857
Y_INTERCEPT = 5949.429

def px_to_x(px: float) -> float:
    return (px - X_LEFT_PX) / DX_PER_UNIT

def x_to_px(x: float) -> float:
    return X_LEFT_PX + DX_PER_UNIT * x

def py_to_tbr(py: float) -> float:
    return (Y_INTERCEPT - py) / (-Y_SLOPE)

def tbr_to_py(tbr: float) -> float:
    return Y_INTERCEPT + Y_SLOPE * tbr

# -----------------------------------------------------------------------------
# 2. Color Response Filters
# -----------------------------------------------------------------------------
def blue_response(arr: np.ndarray) -> np.ndarray:
    """Light blue solid curve (tp = 1 h, circles)."""
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    resp = (b - r) * (b > 140) * (g > 90) * (r < 150) * (b > g)
    resp[:, :int(X_LEFT_PX)] = 0
    resp[:, int(X_RIGHT_PX)+1:] = 0
    resp[:int(Y_TOP_PX), :] = 0
    resp[int(Y_BOTTOM_PX)+1:, :] = 0
    return resp

def red_response(arr: np.ndarray) -> np.ndarray:
    """Red dashed curve (tp = 4 h, squares)."""
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    resp = (r - g) * (r > 130) * (g < 120) * (b < 120) * (r > b + 35)
    resp[:, :int(X_LEFT_PX)] = 0
    resp[:, int(X_RIGHT_PX)+1:] = 0
    resp[:int(Y_TOP_PX), :] = 0
    resp[int(Y_BOTTOM_PX)+1:, :] = 0
    return resp

def navy_response(arr: np.ndarray) -> np.ndarray:
    """Dark navy dash-dot curve (tp = 12 h, triangles)."""
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    resp = (b - 0.5 * (r + g)) * (b > 60) * (b < 170) * (r < 90) * (g < 90) * (b > r + 10) * (b > g + 10)
    resp[:, :int(X_LEFT_PX)] = 0
    resp[:, int(X_RIGHT_PX)+1:] = 0
    resp[:int(Y_TOP_PX), :] = 0
    resp[int(Y_BOTTOM_PX)+1:, :] = 0
    return resp

# -----------------------------------------------------------------------------
# 3. Sub-pixel Marker Extraction
# -----------------------------------------------------------------------------
def extract_marker_roi(resp: np.ndarray, nom_x: float, approx_py: float, win: int = 16):
    px = int(round(x_to_px(nom_x)))
    py = int(round(approx_py))
    
    y0, y1 = max(0, py - win), min(resp.shape[0], py + win + 1)
    x0, x1 = max(0, px - win), min(resp.shape[1], px + win + 1)
    sub = resp[y0:y1, x0:x1].copy()
    
    max_w = np.max(sub)
    if max_w < 10:
        return None
    # Suppress background noise
    sub[sub < 0.40 * max_w] = 0.0
    tot = np.sum(sub)
    if tot == 0:
        return None
    
    y_idx, x_idx = np.indices(sub.shape)
    cy = y0 + np.sum(y_idx * sub) / tot
    cx = x0 + np.sum(x_idx * sub) / tot
    
    det_x = px_to_x(cx)
    det_tbr = py_to_tbr(cy)
    
    # Also evaluate peak at nominal px column (+/- 1 px)
    nom_col = resp[:, max(0, px-1):min(resp.shape[1], px+2)]
    col_prof = nom_col.mean(axis=1)
    # search around cy
    s_y0, s_y1 = max(0, int(round(cy))-8), min(len(col_prof), int(round(cy))+9)
    slice_peak_py = s_y0 + np.argmax(col_prof[s_y0:s_y1])
    slice_tbr = py_to_tbr(slice_peak_py)
    
    return {
        "cx_px": float(cx),
        "cy_px": float(cy),
        "detected_x": float(det_x),
        "marker_tbr": float(det_tbr),
        "slice_tbr": float(slice_tbr),
        "tbr_final": float(round(0.5 * (det_tbr + slice_tbr), 4)),
    }

def main():
    print(f"Loading image from: {IMAGE_PATH}")
    img = Image.open(IMAGE_PATH)
    arr = np.array(img, dtype=np.float32)
    print(f"Image loaded: {img.size[0]} x {img.size[1]} pixels, mode={img.mode}")

    resp_blue = blue_response(arr)
    resp_red = red_response(arr)
    resp_navy = navy_response(arr)

    # -------------------------------------------------------------------------
    # 4. Extract Literature Discrete Markers
    # -------------------------------------------------------------------------
    markers_spec = [
        # (curve_name, tp_hours, resp_map, [(nom_x, approx_py), ...])
        ("tp_1h", 1.0, resp_blue, [
            (0.30, 115.0),
            (0.50, 618.0),
            (0.80, 900.0),
            (1.00, 991.0),
            (1.50, 1119.0),
            (2.00, 1182.0),
            (2.50, 1220.0),
            (3.00, 1244.0),
            (4.00, 1276.0),
            (5.00, 1293.0),
        ]),
        ("tp_4h", 4.0, resp_red, [
            (0.50, 419.0),
            (0.80, 775.0),
            (1.00, 894.0),
            (1.50, 1052.0),
            (2.00, 1133.0),
            (2.50, 1179.0),
            (3.00, 1212.0),
            (4.00, 1251.0),
            (5.00, 1275.0),
        ]),
        ("tp_12h", 12.0, resp_navy, [
            (0.80, 446.0),
            (1.00, 632.0),
            (1.50, 878.0),
            (2.00, 1002.0),
            (2.50, 1076.0),
            (3.00, 1124.0),
            (4.00, 1184.0),
            (5.00, 1222.0),
        ]),
    ]

    all_markers = []
    marker_dict = {}

    for curve_name, tp, resp, points in markers_spec:
        print(f"\nProcessing curve: {curve_name} (tp = {tp} h)")
        curve_data = []
        for nom_x, approx_py in points:
            res = extract_marker_roi(resp, nom_x, approx_py)
            if res is not None:
                row = {
                    "curve": curve_name,
                    "tp_hours": tp,
                    "eta_f_fb_pct": nom_x,
                    "detected_x_pct": round(res["detected_x"], 4),
                    "marker_tbr": round(res["marker_tbr"], 4),
                    "slice_tbr": round(res["slice_tbr"], 4),
                    "required_tbr": res["tbr_final"],
                    "pixel_x": round(res["cx_px"], 2),
                    "pixel_y": round(res["cy_px"], 2),
                }
                all_markers.append(row)
                curve_data.append(row)
                print(f"  nom_x={nom_x:4.2f}% -> det_x={res['detected_x']:6.4f}%, marker_TBR={res['marker_tbr']:6.4f}, final_TBR={res['tbr_final']:6.4f}")
            else:
                print(f"  WARNING: Failed to detect marker at nom_x={nom_x}%")
        marker_dict[curve_name] = curve_data

    df_markers = pd.DataFrame(all_markers)
    markers_csv_path = OUTPUT_DIR / "Fig04_literature_digitized.csv"
    df_markers.to_csv(markers_csv_path, index=False)
    print(f"\nSaved discrete markers to: {markers_csv_path}")

    # -------------------------------------------------------------------------
    # 5. Continuous Curve Digitization & Monotonic PCHIP Spline Reconstruction
    # -------------------------------------------------------------------------
    # High-density grid from 0.10% to 5.00% at step = 0.01%
    dense_grid = np.round(np.arange(0.10, 5.001, 0.01), 4)
    dense_df = pd.DataFrame({"eta_f_fb_pct": dense_grid})

    splines = {}
    for curve_name, tp, _, _ in markers_spec:
        c_rows = [m for m in all_markers if m["curve"] == curve_name]
        c_x = np.array([m["eta_f_fb_pct"] for m in c_rows])
        c_y = np.array([m["required_tbr"] for m in c_rows])
        
        # PCHIP monotonic cubic spline (preserves strictly decreasing physics)
        pchip = scipy.interpolate.PchipInterpolator(c_x, c_y)
        splines[curve_name] = pchip

        # Evaluate on dense grid within valid range
        col_name = f"TBR_{curve_name}"
        x_min, x_max = c_x.min(), c_x.max()
        dense_y = np.where((dense_grid >= x_min) & (dense_grid <= x_max), pchip(dense_grid), np.nan)
        dense_df[col_name] = np.round(dense_y, 4)

    dense_csv_path = OUTPUT_DIR / "Fig04_literature_dense_curves.csv"
    dense_df.to_csv(dense_csv_path, index=False)
    print(f"Saved dense continuous curves (step=0.01%) to: {dense_csv_path}")

    # -------------------------------------------------------------------------
    # 6. YAML Export for V&V Framework Ingestion
    # -------------------------------------------------------------------------
    yaml_data = {
        "metadata": {
            "source_figure": "Abdou 2021 Figure 4",
            "paper": "Physics and technology considerations for the deuterium-tritium fuel cycle and conditions for tritium fuel self sufficiency",
            "citation": "Nuclear Fusion 61 (2021) 013001",
            "doi": "10.1088/1741-4326/abbf35",
            "description": "Required TBR as a function of the core product (eta_f * f_b) for different IFC exhaust processing times (tp = 1, 4, 12 h)",
            "fixed_parameters": {
                "P_fus_MW": 3000.0,
                "AF_pct": 50.0,
                "t_r_hours": 24.0,
                "q_fail_pct": 25.0,
                "t_d_years": 5.0,
                "t_d_hours": 43830.0,
                "f_DIR": 0.0,
                "tau_BZ_days": 1.0,
                "tau_TES_days": 1.0,
            },
        },
        "curves": {},
    }

    for curve_name, tp, _, _ in markers_spec:
        c_rows = [m for m in all_markers if m["curve"] == curve_name]
        yaml_data["curves"][curve_name] = {
            "tp_hours": tp,
            "data_points": [
                {
                    "eta_f_fb_pct": float(r["eta_f_fb_pct"]),
                    "required_tbr": float(r["required_tbr"]),
                }
                for r in c_rows
            ],
        }

    yaml_path = OUTPUT_DIR / "Fig04_literature_digitized.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, sort_keys=False, indent=2)
    print(f"Saved YAML benchmark data to: {yaml_path}")

    # -------------------------------------------------------------------------
    # 7. Side-by-Side Comparison with TRICYS Solver Simulation
    # -------------------------------------------------------------------------
    comparison_rows = []
    if SIM_CSV.exists():
        sim_df = pd.read_csv(SIM_CSV)
        # Determine tp_hours and core_product_pct
        if "f_b" in sim_df.columns and "eta_f" in sim_df.columns:
            sim_df["core_product_pct"] = (sim_df["f_b"] * sim_df["eta_f"] * 100.0).round(2)
        if "comp9_ISS.tau_9" in sim_df.columns:
            sim_df["tp_hours"] = sim_df["comp9_ISS.tau_9"].apply(lambda t: 1.0 if t < 1.0 else (4.0 if t < 6.0 else 12.0))
        elif "name" in sim_df.columns:
            sim_df["tp_hours"] = sim_df["name"].apply(lambda n: 1.0 if "tp1h" in str(n) else (12.0 if "tp12h" in str(n) else 4.0))

        for _, sim_row in sim_df.iterrows():
            tp = sim_row["tp_hours"]
            x_pct = sim_row["core_product_pct"]
            tbr_sim = sim_row["Required_TBR"]
            
            c_name = f"tp_{int(tp)}h"
            # find matching literature marker
            match = df_markers[(df_markers["tp_hours"] == tp) & (np.isclose(df_markers["eta_f_fb_pct"], x_pct, atol=0.05))]
            if not match.empty:
                tbr_lit = match.iloc[0]["required_tbr"]
            else:
                # Interpolate from spline
                if c_name in splines:
                    tbr_lit = float(splines[c_name](x_pct))
                else:
                    tbr_lit = np.nan

            delta_tbr = abs(tbr_sim - tbr_lit)
            rel_err_pct = (delta_tbr / tbr_lit) * 100.0 if tbr_lit > 0 else np.nan

            comparison_rows.append({
                "case_name": sim_row.get("name", f"tp{int(tp)}h_{x_pct}pct"),
                "tp_hours": tp,
                "core_product_pct": x_pct,
                "TBR_TRICYS_sim": round(tbr_sim, 5),
                "TBR_Abdou2021_lit": round(tbr_lit, 4),
                "delta_TBR": round(delta_tbr, 5),
                "rel_error_pct": round(rel_err_pct, 3),
            })

        comp_df = pd.DataFrame(comparison_rows).sort_values(["tp_hours", "core_product_pct"])
        comp_csv_path = OUTPUT_DIR / "Fig04_literature_comparison.csv"
        comp_df.to_csv(comp_csv_path, index=False)
        print(f"\nSaved comparison table to: {comp_csv_path}")

        print("\n=== V&V Summary: TRICYS vs Abdou 2021 Literature ===")
        print(comp_df.to_string(index=False))
        print(f"\nMax Delta TBR: {comp_df['delta_TBR'].max():.4f}")
        print(f"Mean Delta TBR: {comp_df['delta_TBR'].mean():.4f}")
        print(f"Max Relative Error: {comp_df['rel_error_pct'].max():.2f}%")
        print(f"Mean Relative Error: {comp_df['rel_error_pct'].mean():.2f}%")

    # -------------------------------------------------------------------------
    # 8. Visual Verification: Image Overlay & Audit Figure
    # -------------------------------------------------------------------------
    print("\nGenerating visual verification plots...")

    # Plot 1: Direct Overlay on Fig04.png
    fig_overlay, ax_ov = plt.subplots(figsize=(10, 8), dpi=300)
    ax_ov.imshow(img)

    # Plot detected markers and splines on top of original pixels
    colors = {"tp_1h": "#00E5FF", "tp_4h": "#FF1744", "tp_12h": "#FFD600"}
    symbols = {"tp_1h": "o", "tp_4h": "s", "tp_12h": "^"}

    for curve_name, tp, _, _ in markers_spec:
        c_rows = [m for m in all_markers if m["curve"] == curve_name]
        px_list = [x_to_px(r["eta_f_fb_pct"]) for r in c_rows]
        py_list = [tbr_to_py(r["required_tbr"]) for r in c_rows]

        # Spline curve in pixel space
        grid_x = np.linspace(c_rows[0]["eta_f_fb_pct"], c_rows[-1]["eta_f_fb_pct"], 300)
        grid_tbr = splines[curve_name](grid_x)
        grid_px = x_to_px(grid_x)
        grid_py = tbr_to_py(grid_tbr)

        ax_ov.plot(grid_px, grid_py, color=colors[curve_name], lw=1.8, alpha=0.9,
                   label=f"Digitized {curve_name} (tp={tp}h)")
        ax_ov.scatter(px_list, py_list, color=colors[curve_name], edgecolor="black",
                      s=45, marker=symbols[curve_name], zorder=10, lw=1.2)

    ax_ov.set_title("Abdou 2021 Fig 04: Digitized Markers & Splines Pixel Overlay Verification",
                    fontsize=12, fontweight="bold", pad=12)
    ax_ov.legend(loc="upper right", fontsize=9, framealpha=0.85)
    ax_ov.axis("off")
    plt.tight_layout()

    overlay_path = REPO_ROOT / "v&v" / "Abdou2021" / "Fig04_digitization_overlay.png"
    plt.savefig(overlay_path, dpi=300, bbox_inches="tight")
    plt.close(fig_overlay)
    print(f"Saved overlay image to: {overlay_path}")

    # Plot 2: Scientific Multi-Panel Verification Report
    fig_audit, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    # Left: Digitized Ground Truth vs Model Simulation
    ax1 = axes[0]
    ax1.axhspan(1.00, 1.05, color="#A5D6A7", alpha=0.45, label=r"Attained with High Confidence ($\mathrm{TBR}_R \leq 1.05$)")
    ax1.axhspan(1.05, 1.15, color="#C8E6C9", alpha=0.35, label=r"Possible Self-Sufficiency Window ($1.05 < \mathrm{TBR}_R \leq 1.15$)")
    ax1.axhline(1.15, color="#2E7D32", ls="--", lw=1.0)
    ax1.axhline(1.05, color="#1B5E20", ls=":", lw=1.0)

    curve_styles = [
        ("tp_1h", 1.0, "#1E88E5", "o", "-", r"$t_p = 1$ h (Abdou 2021)"),
        ("tp_4h", 4.0, "#D32F2F", "s", "--", r"$t_p = 4$ h Ref (Abdou 2021)"),
        ("tp_12h", 12.0, "#0D47A1", "^", "-.", r"$t_p = 12$ h (Abdou 2021)"),
    ]

    for c_name, tp, col, m, ls, lbl in curve_styles:
        c_rows = [m for m in all_markers if m["curve"] == c_name]
        xs = [r["eta_f_fb_pct"] for r in c_rows]
        ys = [r["required_tbr"] for r in c_rows]
        
        # Plot continuous dense line
        dense_x = np.linspace(xs[0], xs[-1], 200)
        dense_y = splines[c_name](dense_x)
        ax1.plot(dense_x, dense_y, color=col, ls=ls, lw=2.0, label=lbl)
        ax1.scatter(xs, ys, color=col, edgecolor="black", s=50, marker=m, zorder=5)

    # Overlay TRICYS simulation points if available
    if len(comparison_rows) > 0:
        sim_col = {"1.0": "#64B5F6", "4.0": "#EF5350", "12.0": "#3949AB"}
        for tp in [1.0, 4.0, 12.0]:
            sub_c = [r for r in comparison_rows if r["tp_hours"] == tp]
            if sub_c:
                ax1.scatter([r["core_product_pct"] for r in sub_c],
                            [r["TBR_TRICYS_sim"] for r in sub_c],
                            color="none", edgecolor="black", s=110, lw=1.5,
                            marker="x", zorder=6, label=f"TRICYS Sim ($t_p={int(tp)}$ h)")

    ax1.set_xlim(0.0, 5.2)
    ax1.set_ylim(1.00, 1.30)
    ax1.set_xlabel(r"Core Product $\eta_f f_b$ (%)", fontweight="bold", fontsize=11)
    ax1.set_ylabel(r"Required TBR ($\mathrm{TBR}_R$)", fontweight="bold", fontsize=11)
    ax1.set_title("Ground Truth Digitization vs TRICYS Model Simulation", fontweight="bold", fontsize=11)
    ax1.grid(True, ls=":", alpha=0.6)
    ax1.legend(loc="upper right", fontsize=8.2)

    # Right: Relative Error & Deviation Distribution
    ax2 = axes[1]
    if len(comparison_rows) > 0:
        for c_name, tp, col, m, ls, _ in curve_styles:
            sub_c = [r for r in comparison_rows if r["tp_hours"] == tp]
            if sub_c:
                ax2.plot([r["core_product_pct"] for r in sub_c],
                         [r["rel_error_pct"] for r in sub_c],
                         color=col, marker=m, ls=ls, lw=1.8, ms=7,
                         label=f"$t_p = {int(tp)}$ h error (%)")

        ax2.axhline(0.5, color="gray", ls="--", lw=1.0, label="0.5% Threshold")
        ax2.axhline(1.0, color="red", ls=":", lw=1.0, label="1.0% Threshold")
        ax2.set_xlim(0.0, 5.2)
        ax2.set_ylim(0.0, 1.2)
        ax2.set_xlabel(r"Core Product $\eta_f f_b$ (%)", fontweight="bold", fontsize=11)
        ax2.set_ylabel(r"Relative Error $\Delta \mathrm{TBR} / \mathrm{TBR}_{\mathrm{lit}}$ (%)", fontweight="bold", fontsize=11)
        ax2.set_title("TRICYS vs Literature Relative Discrepancy", fontweight="bold", fontsize=11)
        ax2.grid(True, ls=":", alpha=0.6)
        ax2.legend(loc="upper right", fontsize=8.5)
    else:
        ax2.text(0.5, 0.5, "No Simulation Data Found", ha="center", va="center")

    plt.tight_layout()
    audit_fig_path = FIG_DIR / "Fig04_digitization_verification.png"
    plt.savefig(audit_fig_path, dpi=300)
    plt.close(fig_audit)
    print(f"Saved audit comparison plot to: {audit_fig_path}")

    print("\nDigitization and V&V pipeline completed successfully!")

if __name__ == "__main__":
    main()
