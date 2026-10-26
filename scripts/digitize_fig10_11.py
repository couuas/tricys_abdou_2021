#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""High-Fidelity Digitization of Abdou 2021 Figure 10 and Figure 11.

Fig10: Tritium Start-up Inventory vs Core Product (tp = 1, 4, 12 h)
Fig11: Start-up Inventory Reduction via DIR Fraction (eta_f*fb = 0.5, 1, 2, 3%)
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

# Color filters
blue_f = lambda rgb: float(rgb[2] - rgb[0]) if (rgb[2] > 140 and rgb[1] > 90 and rgb[0] < 140 and rgb[2] > rgb[1]) else 0.0
red_f = lambda rgb: float(rgb[0] - max(rgb[1], rgb[2])) if (rgb[0] > 140 and rgb[1] < 100 and rgb[2] < 100) else 0.0
navy_f = lambda rgb: float(rgb[2] - 0.5*(rgb[0]+rgb[1])) if (rgb[2] > 60 and rgb[2] < 160 and rgb[0] < 80 and rgb[1] < 80) else 0.0
green_f = lambda rgb: float(rgb[1] - max(rgb[0], rgb[2])) if (rgb[1] > rgb[0]+8 and rgb[1] > rgb[2]+8 and rgb[0] < 120 and rgb[1] < 140) else 0.0
mag_f = lambda rgb: float(min(rgb[0], rgb[2]) - rgb[1]) if (rgb[0] > 110 and rgb[2] > 100 and rgb[1] < 100) else 0.0

def digitize_fig10():
    img_path = IMG_DIR / "Fig10.png"
    img = Image.open(img_path)
    arr = np.array(img, dtype=np.float32)

    x_left, x_right = 220.0, 1872.0
    y_top, y_bottom = 25.0, 1282.0
    dx = (x_right - x_left) / 5.0
    dy = (y_bottom - y_top) / 40.0

    def val_to_px(x, y):
        return x_left + x * dx, y_bottom - y * dy

    def px_to_val(px, py):
        return (px - x_left) / dx, (y_bottom - py) / dy

    curves_spec = [
        {"name": "tp_1h", "tp_hours": 1.0, "symbol": "circle", "color_filter": blue_f,
         "points": [(0.5, 29.6), (0.8, 19.0), (1.0, 15.3), (1.5, 10.4), (2.0, 8.0), (2.5, 6.6), (3.0, 5.7), (4.0, 4.5), (5.0, 3.8)]},
        {"name": "tp_4h", "tp_hours": 4.0, "symbol": "square", "color_filter": red_f,
         "points": [(0.8, 26.8), (1.0, 21.6), (1.5, 14.6), (2.0, 11.2), (2.5, 9.2), (3.0, 7.8), (4.0, 6.1), (5.0, 5.0)]},
        {"name": "tp_12h", "tp_hours": 12.0, "symbol": "triangle", "color_filter": navy_f,
         "points": [(1.0, 38.6), (1.5, 26.0), (2.0, 19.8), (2.5, 16.0), (3.0, 13.5), (4.0, 10.4), (5.0, 8.6)]},
    ]

    rows = []
    win = 16
    print("\n==================== Processing Fig10 ====================")
    for c in curves_spec:
        print(f"Curve: {c['name']}")
        for x_nom, y_approx in c["points"]:
            px, py = val_to_px(x_nom, y_approx)
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

            det_x, det_y = px_to_val(cx, cy)
            row = {
                "figure": "Fig10",
                "curve": c["name"],
                "tp_hours": c["tp_hours"],
                "marker_symbol": c["symbol"],
                "eta_f_fb_nominal_pct": round(float(x_nom), 2),
                "eta_f_fb_detected_pct": round(float(det_x), 3),
                "startup_inventory_IS0_kg": round(float(det_y), 3),
                "pixel_x": round(float(cx), 2),
                "pixel_y": round(float(cy), 2),
            }
            rows.append(row)
            print(f"  x={x_nom:4.2f}% -> det_x={det_x:5.3f}%, IS0={det_y:.3f} kg")

    df = pd.DataFrame(rows)
    out_csv = OUT_DIR / "Fig10_literature_markers.csv"
    df.to_csv(out_csv, index=False)
    print(f"Saved Fig10 markers ({len(df)} points) to {out_csv}")

    fig, ax = plt.subplots(figsize=(10, 8), dpi=250)
    ax.imshow(img)
    cmap = {"tp_1h": "#00E5FF", "tp_4h": "#FF1744", "tp_12h": "#FFD600"}
    for c in curves_spec:
        sub = df[df["curve"] == c["name"]]
        ax.plot(sub["pixel_x"], sub["pixel_y"], color=cmap[c["name"]], lw=1.8, alpha=0.9, label=c["name"])
        ax.scatter(sub["pixel_x"], sub["pixel_y"], color="none", edgecolor=cmap[c["name"]], s=70, lw=2.0, zorder=5)
    ax.set_title("Abdou 2021 Fig 10: Discrete Markers Overlay Verification", fontsize=12, fontweight="bold")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.axis("off")
    plt.tight_layout()
    overlay_out = IMG_DIR / "Fig10_digitization_overlay.png"
    plt.savefig(overlay_out, dpi=250, bbox_inches="tight")
    plt.close(fig)

def digitize_fig11():
    img_path = IMG_DIR / "Fig11.png"
    img = Image.open(img_path)
    arr = np.array(img, dtype=np.float32)

    x_left, x_right = 211.0, 1867.0
    y_top, y_bottom = 15.0, 1286.0
    dx = (x_right - x_left) / 80.0
    dy = (y_bottom - y_top) / 45.0

    def val_to_px(dir_v, y):
        return x_left + (dir_v - 10.0) * dx, y_bottom - y * dy

    def px_to_val(px, py):
        return 10.0 + (px - x_left) / dx, (y_bottom - py) / dy

    curves_spec = [
        {"name": "eta_f_fb_0.5pct", "eta_f_fb_pct": 0.5, "symbol": "diamond", "color_filter": green_f,
         "points": [(10.0, 40.7), (30.0, 37.1), (50.0, 33.6), (70.0, 30.2), (90.0, 26.6)]},
        {"name": "eta_f_fb_1.0pct", "eta_f_fb_pct": 1.0, "symbol": "square", "color_filter": red_f,
         "points": [(10.0, 20.8), (30.0, 19.0), (50.0, 17.3), (70.0, 15.5), (90.0, 13.8)]},
        {"name": "eta_f_fb_2.0pct", "eta_f_fb_pct": 2.0, "symbol": "circle", "color_filter": navy_f,
         "points": [(10.0, 10.8), (30.0, 9.9), (50.0, 9.1), (70.0, 8.3), (90.0, 7.4)]},
        {"name": "eta_f_fb_3.0pct", "eta_f_fb_pct": 3.0, "symbol": "cross", "color_filter": mag_f,
         "points": [(10.0, 7.5), (30.0, 7.0), (50.0, 6.4), (70.0, 5.8), (90.0, 5.2)]},
    ]

    rows = []
    win = 16
    print("\n==================== Processing Fig11 ====================")
    for c in curves_spec:
        print(f"Curve: {c['name']}")
        for x_nom, y_approx in c["points"]:
            px, py = val_to_px(x_nom, y_approx)
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

            det_x, det_y = px_to_val(cx, cy)
            row = {
                "figure": "Fig11",
                "curve": c["name"],
                "eta_f_fb_pct": c["eta_f_fb_pct"],
                "marker_symbol": c["symbol"],
                "DIR_nominal_pct": round(float(x_nom), 1),
                "DIR_detected_pct": round(float(det_x), 1),
                "startup_inventory_IS0_kg": round(float(det_y), 3),
                "pixel_x": round(float(cx), 2),
                "pixel_y": round(float(cy), 2),
            }
            rows.append(row)
            print(f"  DIR={x_nom:4.1f}% -> det_DIR={det_x:4.1f}%, IS0={det_y:.3f} kg")

    df = pd.DataFrame(rows)
    out_csv = OUT_DIR / "Fig11_literature_markers.csv"
    df.to_csv(out_csv, index=False)
    print(f"Saved Fig11 markers ({len(df)} points) to {out_csv}")

    fig, ax = plt.subplots(figsize=(10, 8), dpi=250)
    ax.imshow(img)
    cmap = {"eta_f_fb_0.5pct": "#76FF03", "eta_f_fb_1.0pct": "#FF1744", "eta_f_fb_2.0pct": "#00E5FF", "eta_f_fb_3.0pct": "#E040FB"}
    for c in curves_spec:
        sub = df[df["curve"] == c["name"]]
        ax.plot(sub["pixel_x"], sub["pixel_y"], color=cmap[c["name"]], lw=1.8, alpha=0.9, label=c["name"])
        ax.scatter(sub["pixel_x"], sub["pixel_y"], color="none", edgecolor=cmap[c["name"]], s=70, lw=2.0, zorder=5)
    ax.set_title("Abdou 2021 Fig 11: Discrete Markers Overlay Verification", fontsize=12, fontweight="bold")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.axis("off")
    plt.tight_layout()
    overlay_out = IMG_DIR / "Fig11_digitization_overlay.png"
    plt.savefig(overlay_out, dpi=250, bbox_inches="tight")
    plt.close(fig)

def main():
    digitize_fig10()
    digitize_fig11()

if __name__ == "__main__":
    main()
