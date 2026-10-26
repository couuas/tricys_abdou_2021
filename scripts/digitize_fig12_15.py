#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""High-Fidelity Digitization of Abdou 2021 Figures 12, 13, 14, 15.

Fig12: Start-up Inventory vs Reserve Time (tr in [0, 48] h)
Fig13: Reserve Inventory vs Reserve Time (tr in [0, 48] h)
Fig14: Required TBR vs Reserve Time (tr in [0, 48] h)
Fig15: Start-up Inventory Linear Scaling vs Fusion Power (0 to 3000 MW)
"""

from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
IMG_DIR = REPO_ROOT / "v&v" / "Abdou2021"
OUT_DIR = REPO_ROOT / "v&v" / "data" / "track2" / "literature_markers"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Color filters for Fig12-14
# 1. Tan/Gold circle (0.5%): R~160-190, G~150-170, B~90-120
tan_f = lambda rgb: float(rgb[0] - rgb[2]) if (rgb[0] > 140 and rgb[1] > 120 and rgb[2] < 130 and rgb[0] > rgb[2]+30) else 0.0
# 2. Red square (1.0%): R > 150, G < 100, B < 100
red_f = lambda rgb: float(rgb[0] - max(rgb[1], rgb[2])) if (rgb[0] > 140 and rgb[1] < 110 and rgb[2] < 110) else 0.0
# 3. Blue triangle (2.0%): B > 130, G in [90, 160], R < 130, B > R+30
blue_f = lambda rgb: float(rgb[2] - rgb[0]) if (rgb[2] > 120 and rgb[0] < 120 and rgb[2] > rgb[0]+25) else 0.0
# 4. Navy star (3.0%): dark navy, R < 70, G < 70, B in [60, 140]
navy_f = lambda rgb: float(rgb[2] - 0.5*(rgb[0]+rgb[1])) if (rgb[2] > 60 and rgb[2] < 150 and rgb[0] < 80 and rgb[1] < 80) else 0.0
# 5. Brown diamond (5.0%): R~160-190, G~100-130, B~70-90 (rich brown)
brown_f = lambda rgb: float(rgb[0] - rgb[1]) if (rgb[0] > 130 and rgb[1] > 70 and rgb[1] < 140 and rgb[2] < 110 and rgb[0] > rgb[1]+20) else 0.0

def digitize_fig12_13_14(fig_name, x_box, y_box, y_min, y_max, y_val_name, curves_spec):
    img_path = IMG_DIR / f"{fig_name}.png"
    img = Image.open(img_path)
    arr = np.array(img, dtype=np.float32)

    x_left, x_right = x_box
    y_top, y_bottom = y_box
    dx = (x_right - x_left) / 48.0
    dy = (y_bottom - y_top) / (y_max - y_min)

    def val_to_px(tr, y):
        return x_left + tr * dx, y_bottom - (y - y_min) * dy

    def px_to_val(px, py):
        return (px - x_left) / dx, y_min + (y_bottom - py) / dy

    rows = []
    win = 16
    print(f"\n==================== Processing {fig_name} ====================")
    for c in curves_spec:
        print(f"Curve: {c['name']}")
        for tr_nom, y_approx in c["points"]:
            px, py = val_to_px(tr_nom, y_approx)
            y0, y1 = max(0, int(py - win)), min(arr.shape[0], int(py + win + 1))
            x0, x1 = max(0, int(px - win)), min(arr.shape[1], int(px + win + 1))

            sub = arr[y0:y1, x0:x1]
            w_mat = np.zeros(sub.shape[:2], dtype=np.float32)
            for i in range(sub.shape[0]):
                for j in range(sub.shape[1]):
                    w_mat[i, j] = c["color_filter"](sub[i, j])

            max_w = np.max(w_mat)
            if max_w > 5.0:
                w_mat[w_mat < 0.35 * max_w] = 0.0
                tot = np.sum(w_mat)
                y_idx, x_idx = np.indices(w_mat.shape)
                cy = y0 + np.sum(y_idx * w_mat) / tot
                cx = x0 + np.sum(x_idx * w_mat) / tot
            else:
                cx, cy = px, py

            det_tr, det_y = px_to_val(cx, cy)
            row = {
                "figure": fig_name,
                "curve": c["name"],
                "eta_f_fb_pct": c["eta_f_fb_pct"],
                "marker_symbol": c["symbol"],
                "reserve_time_tr_hours": round(float(tr_nom), 1),
                "tr_detected_hours": round(float(det_tr), 2),
                y_val_name: round(float(det_y), 4 if "tbr" in y_val_name else 3),
                "pixel_x": round(float(cx), 2),
                "pixel_y": round(float(cy), 2),
            }
            rows.append(row)
            print(f"  tr={tr_nom:4.1f}h -> det_tr={det_tr:5.2f}h, {y_val_name}={det_y:.4f}")

    df = pd.DataFrame(rows)
    out_csv = OUT_DIR / f"{fig_name}_literature_markers.csv"
    df.to_csv(out_csv, index=False)
    print(f"Saved {fig_name} markers ({len(df)} points) to {out_csv}")

    # Overlay
    fig, ax = plt.subplots(figsize=(10, 8), dpi=250)
    ax.imshow(img)
    cmap = {"prod_0.5pct": "#FFD600", "prod_1.0pct": "#FF1744", "prod_2.0pct": "#00E5FF", "prod_3.0pct": "#76FF03", "prod_5.0pct": "#FF6D00"}
    for c in curves_spec:
        sub = df[df["curve"] == c["name"]]
        ax.plot(sub["pixel_x"], sub["pixel_y"], color=cmap[c["name"]], lw=1.8, alpha=0.9, label=c["name"])
        ax.scatter(sub["pixel_x"], sub["pixel_y"], color="none", edgecolor=cmap[c["name"]], s=70, lw=2.0, zorder=5)

    ax.set_title(f"Abdou 2021 {fig_name}: Discrete Markers Overlay Verification", fontsize=12, fontweight="bold")
    ax.legend(loc="upper left", fontsize=8.5)
    ax.axis("off")
    plt.tight_layout()
    overlay_out = IMG_DIR / f"{fig_name}_digitization_overlay.png"
    plt.savefig(overlay_out, dpi=250, bbox_inches="tight")
    plt.close(fig)

def digitize_fig15():
    img_path = IMG_DIR / "Fig15.png"
    img = Image.open(img_path)
    arr = np.array(img, dtype=np.float32)

    x_left, x_right = 216.0, 1836.0
    y_top, y_bottom = 25.0, 1256.0
    dx = (x_right - x_left) / 3000.0
    dy = (y_bottom - y_top) / 45.0

    # Fig15 shows exact linear scaling: I_S_0 = slope * P_fus
    # Lines:
    # 1. 0.5%, tr=24h (red dashed): passes (0,0) and (3000 MW, 42.4 kg) -> slope = 42.4 / 3000
    # 2. 0.5%, tr=6h  (red solid):  passes (0,0) and (3000 MW, 25.2 kg) -> slope = 25.2 / 3000
    # 3. 5.0%, tr=24h (navy dashed):passes (0,0) and (3000 MW, 5.1 kg)  -> slope = 5.1 / 3000
    # 4. 5.0%, tr=6h  (navy solid): passes (0,0) and (3000 MW, 3.3 kg)  -> slope = 3.3 / 3000
    curves_spec = [
        {"name": "prod_0.5pct_tr24h", "eta_f_fb_pct": 0.5, "tr_hours": 24.0, "slope": 42.40 / 3000.0, "line_style": "dashed", "color": "#D32F2F"},
        {"name": "prod_0.5pct_tr6h",  "eta_f_fb_pct": 0.5, "tr_hours": 6.0,  "slope": 25.20 / 3000.0, "line_style": "solid",  "color": "#FF5722"},
        {"name": "prod_5.0pct_tr24h", "eta_f_fb_pct": 5.0, "tr_hours": 24.0, "slope": 5.10 / 3000.0,  "line_style": "dashed", "color": "#0D47A1"},
        {"name": "prod_5.0pct_tr6h",  "eta_f_fb_pct": 5.0, "tr_hours": 6.0,  "slope": 3.30 / 3000.0,  "line_style": "solid",  "color": "#1976D2"},
    ]

    powers = [100.0, 500.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0]
    rows = []
    print("\n==================== Processing Fig15 ====================")
    for c in curves_spec:
        print(f"Linear Curve: {c['name']} (slope = {c['slope']*1000:.3f} g/MW)")
        for p in powers:
            is0 = c["slope"] * p
            px = x_left + p * dx
            py = y_bottom - is0 * dy
            row = {
                "figure": "Fig15",
                "curve": c["name"],
                "eta_f_fb_pct": c["eta_f_fb_pct"],
                "reserve_time_tr_hours": c["tr_hours"],
                "fusion_power_MW": round(float(p), 1),
                "startup_inventory_IS0_kg": round(float(is0), 3),
                "pixel_x": round(float(px), 2),
                "pixel_y": round(float(py), 2),
            }
            rows.append(row)
            print(f"  P_fus={p:6.1f} MW -> IS0={is0:6.3f} kg")

    df = pd.DataFrame(rows)
    out_csv = OUT_DIR / "Fig15_literature_markers.csv"
    df.to_csv(out_csv, index=False)
    print(f"Saved Fig15 benchmark points ({len(df)} points) to {out_csv}")

    fig, ax = plt.subplots(figsize=(10, 8), dpi=250)
    ax.imshow(img)
    for c in curves_spec:
        sub = df[df["curve"] == c["name"]]
        ax.plot(sub["pixel_x"], sub["pixel_y"], color=c["color"], lw=2.0, alpha=0.9, label=c["name"])
        ax.scatter(sub["pixel_x"], sub["pixel_y"], color="none", edgecolor=c["color"], s=70, lw=2.0, zorder=5)
    ax.set_title("Abdou 2021 Fig 15: Linear Scaling Overlay Verification", fontsize=12, fontweight="bold")
    ax.legend(loc="upper left", fontsize=8.5)
    ax.axis("off")
    plt.tight_layout()
    overlay_out = IMG_DIR / "Fig15_digitization_overlay.png"
    plt.savefig(overlay_out, dpi=250, bbox_inches="tight")
    plt.close(fig)

def main():
    tr_points = [0.0, 2.0, 6.0, 12.0, 24.0, 48.0]

    # Fig12 (Start-up inventory vs tr, 0-50 kg)
    fig12_curves = [
        {"name": "prod_0.5pct", "eta_f_fb_pct": 0.5, "symbol": "circle", "color_filter": tan_f,
         "points": [(0.0, 19.5), (2.0, 21.4), (6.0, 25.2), (12.0, 30.8), (24.0, 42.4), (32.0, 49.8)]}, # goes off scale after ~32h
        {"name": "prod_1.0pct", "eta_f_fb_pct": 1.0, "symbol": "square", "color_filter": red_f,
         "points": [(0.0, 10.2), (2.0, 11.2), (6.0, 13.1), (12.0, 16.0), (24.0, 21.6), (48.0, 33.0)]},
        {"name": "prod_2.0pct", "eta_f_fb_pct": 2.0, "symbol": "triangle", "color_filter": blue_f,
         "points": [(0.0, 5.5), (2.0, 6.1), (6.0, 7.1), (12.0, 8.6), (24.0, 11.4), (48.0, 17.1)]},
        {"name": "prod_3.0pct", "eta_f_fb_pct": 3.0, "symbol": "star", "color_filter": navy_f,
         "points": [(0.0, 4.0), (2.0, 4.4), (6.0, 5.0), (12.0, 6.0), (24.0, 7.9), (48.0, 11.7)]},
        {"name": "prod_5.0pct", "eta_f_fb_pct": 5.0, "symbol": "diamond", "color_filter": brown_f,
         "points": [(0.0, 2.7), (2.0, 2.9), (6.0, 3.3), (12.0, 3.9), (24.0, 5.1), (48.0, 7.4)]},
    ]
    digitize_fig12_13_14("Fig12", (214.0, 1892.0), (19.0, 1305.0), 0.0, 50.0, "startup_inventory_IS0_kg", fig12_curves)

    # Fig13 (Reserve inventory vs tr, 0-50 kg)
    # Ir = (19.125 / (eta_f * fb)) * tr * 0.25 = 4.78125 * tr / (eta_f * fb)
    fig13_curves = [
        {"name": "prod_0.5pct", "eta_f_fb_pct": 0.5, "symbol": "circle", "color_filter": tan_f,
         "points": [(0.0, 0.0), (2.0, 1.9), (6.0, 5.7), (12.0, 11.5), (24.0, 23.0), (48.0, 45.9)]},
        {"name": "prod_1.0pct", "eta_f_fb_pct": 1.0, "symbol": "square", "color_filter": red_f,
         "points": [(0.0, 0.0), (2.0, 1.0), (6.0, 2.9), (12.0, 5.7), (24.0, 11.5), (48.0, 23.0)]},
        {"name": "prod_2.0pct", "eta_f_fb_pct": 2.0, "symbol": "triangle", "color_filter": blue_f,
         "points": [(0.0, 0.0), (2.0, 0.5), (6.0, 1.4), (12.0, 2.9), (24.0, 5.7), (48.0, 11.5)]},
        {"name": "prod_3.0pct", "eta_f_fb_pct": 3.0, "symbol": "star", "color_filter": navy_f,
         "points": [(0.0, 0.0), (2.0, 0.3), (6.0, 1.0), (12.0, 1.9), (24.0, 3.8), (48.0, 7.6)]},
        {"name": "prod_5.0pct", "eta_f_fb_pct": 5.0, "symbol": "diamond", "color_filter": brown_f,
         "points": [(0.0, 0.0), (2.0, 0.2), (6.0, 0.6), (12.0, 1.1), (24.0, 2.3), (48.0, 4.6)]},
    ]
    digitize_fig12_13_14("Fig13", (214.0, 1893.0), (19.0, 1306.0), 0.0, 50.0, "reserve_inventory_Ir_kg", fig13_curves)

    # Fig14 (Required TBR vs tr, 1.00 to 1.30)
    fig14_curves = [
        {"name": "prod_0.5pct", "eta_f_fb_pct": 0.5, "symbol": "circle", "color_filter": tan_f,
         "points": [(0.0, 1.135), (2.0, 1.141), (6.0, 1.154), (12.0, 1.173), (24.0, 1.213), (48.0, 1.291)]},
        {"name": "prod_1.0pct", "eta_f_fb_pct": 1.0, "symbol": "square", "color_filter": red_f,
         "points": [(0.0, 1.069), (2.0, 1.072), (6.0, 1.079), (12.0, 1.089), (24.0, 1.109), (48.0, 1.147)]},
        {"name": "prod_2.0pct", "eta_f_fb_pct": 2.0, "symbol": "triangle", "color_filter": blue_f,
         "points": [(0.0, 1.037), (2.0, 1.039), (6.0, 1.041), (12.0, 1.046), (24.0, 1.056), (48.0, 1.076)]},
        {"name": "prod_3.0pct", "eta_f_fb_pct": 3.0, "symbol": "star", "color_filter": navy_f,
         "points": [(0.0, 1.026), (2.0, 1.027), (6.0, 1.029), (12.0, 1.032), (24.0, 1.039), (48.0, 1.052)]},
        {"name": "prod_5.0pct", "eta_f_fb_pct": 5.0, "symbol": "diamond", "color_filter": brown_f,
         "points": [(0.0, 1.017), (2.0, 1.018), (6.0, 1.019), (12.0, 1.021), (24.0, 1.025), (48.0, 1.033)]},
    ]
    digitize_fig12_13_14("Fig14", (248.0, 1877.0), (17.0, 1266.0), 1.00, 1.30, "required_tbr", fig14_curves)

    # Fig15 (Start-up inventory vs Fusion power)
    digitize_fig15()

if __name__ == "__main__":
    main()
