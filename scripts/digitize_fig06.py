#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""High-Fidelity Digitization of Abdou 2021 Figure 06.

Subject: Mitigation of Required TBR via DIR Bypass
Curves:
- eta_f * fb = 0.5% (olive diamond, dotted)
- eta_f * fb = 1.0% (red square, dashed)
- eta_f * fb = 2.0% (navy circle, solid)
- eta_f * fb = 3.0% (magenta cross, dash-dot)
"""

from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
IMG_PATH = REPO_ROOT / "v&v" / "Abdou2021" / "Fig06.png"
OUT_DIR = REPO_ROOT / "v&v" / "data" / "track2" / "literature_markers"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Coordinate system
X_LEFT = 243.0
X_RIGHT = 1867.0
DX = (X_RIGHT - X_LEFT) / 80.0    # 20.30 px / %

Y_TOP = 18.0
Y_BOTTOM = 1266.0
DY = (Y_BOTTOM - Y_TOP) / 0.25    # 4992.0 px / unit TBR

def val_to_px(dir_val, tbr):
    px = X_LEFT + (dir_val - 10.0) * DX
    py = Y_BOTTOM - (tbr - 1.00) * DY
    return px, py

def px_to_val(px, py):
    dir_val = 10.0 + (px - X_LEFT) / DX
    tbr = 1.00 + (Y_BOTTOM - py) / DY
    return dir_val, tbr

# Markers specifications:
# DIR points: [10, 30, 50, 70, 90]%
curves_spec = [
    {
        "name": "eta_f_fb_0.5pct",
        "eta_f_fb_pct": 0.5,
        "symbol": "diamond",
        # Olive green marker: R~50, G~75, B~54
        "color_filter": lambda rgb: float(rgb[1] - max(rgb[0], rgb[2])) if (rgb[1] > rgb[0]+8 and rgb[1] > rgb[2]+8 and rgb[0] < 120 and rgb[1] < 140) else 0.0,
        "points": [
            (10.0, 1.204),
            (30.0, 1.187),
            (50.0, 1.171),
            (70.0, 1.154),
            (90.0, 1.137),
        ],
    },
    {
        "name": "eta_f_fb_1.0pct",
        "eta_f_fb_pct": 1.0,
        "symbol": "square",
        # Red marker: R > 140, G < 100, B < 100
        "color_filter": lambda rgb: float(rgb[0] - max(rgb[1], rgb[2])) if (rgb[0] > 130 and rgb[1] < 100 and rgb[2] < 100) else 0.0,
        "points": [
            (10.0, 1.104),
            (30.0, 1.096),
            (50.0, 1.087),
            (70.0, 1.078),
            (90.0, 1.070),
        ],
    },
    {
        "name": "eta_f_fb_2.0pct",
        "eta_f_fb_pct": 2.0,
        "symbol": "circle",
        # Navy marker: B > R+15, B > G+15, B in [70, 160], R < 80, G < 80
        "color_filter": lambda rgb: float(rgb[2] - 0.5*(rgb[0]+rgb[1])) if (rgb[2] > 70 and rgb[2] < 160 and rgb[0] < 80 and rgb[1] < 80) else 0.0,
        "points": [
            (10.0, 1.053),
            (30.0, 1.049),
            (50.0, 1.045),
            (70.0, 1.041),
            (90.0, 1.037),
        ],
    },
    {
        "name": "eta_f_fb_3.0pct",
        "eta_f_fb_pct": 3.0,
        "symbol": "cross",
        # Magenta cross: R > 110, B > 100, G < 100
        "color_filter": lambda rgb: float(min(rgb[0], rgb[2]) - rgb[1]) if (rgb[0] > 110 and rgb[2] > 100 and rgb[1] < 100) else 0.0,
        "points": [
            (10.0, 1.037),
            (30.0, 1.034),
            (50.0, 1.032),
            (70.0, 1.029),
            (90.0, 1.026),
        ],
    },
]

def main():
    img = Image.open(IMG_PATH)
    arr = np.array(img, dtype=np.float32)

    rows = []
    win = 16

    for c in curves_spec:
        print(f"\nProcessing Fig06: {c['name']}")
        for dir_nom, tbr_approx in c["points"]:
            px, py = val_to_px(dir_nom, tbr_approx)
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

            det_dir, det_tbr = px_to_val(cx, cy)
            row = {
                "figure": "Fig06",
                "curve": c["name"],
                "eta_f_fb_pct": c["eta_f_fb_pct"],
                "marker_symbol": c["symbol"],
                "DIR_nominal_pct": round(float(dir_nom), 1),
                "DIR_detected_pct": round(float(det_dir), 1),
                "required_tbr": round(float(det_tbr), 4),
                "pixel_x": round(float(cx), 2),
                "pixel_y": round(float(cy), 2),
            }
            rows.append(row)
            print(f"  DIR={dir_nom:4.1f}% -> det_DIR={det_dir:4.1f}%, TBR={det_tbr:.4f}")

    df = pd.DataFrame(rows)
    out_csv = OUT_DIR / "Fig06_literature_markers.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nSaved Fig06 markers ({len(df)} points) to {out_csv}")

    # Overlay plot
    fig, ax = plt.subplots(figsize=(10, 8), dpi=250)
    ax.imshow(img)
    cmap = {"eta_f_fb_0.5pct": "#76FF03", "eta_f_fb_1.0pct": "#FF1744", "eta_f_fb_2.0pct": "#00E5FF", "eta_f_fb_3.0pct": "#E040FB"}
    for c in curves_spec:
        sub = df[df["curve"] == c["name"]]
        ax.plot(sub["pixel_x"], sub["pixel_y"], color=cmap[c["name"]], lw=1.8, alpha=0.9, label=c["name"])
        ax.scatter(sub["pixel_x"], sub["pixel_y"], color="none", edgecolor=cmap[c["name"]], s=70, lw=2.0, zorder=5)

    ax.set_title("Abdou 2021 Fig 06: Discrete Markers Overlay Verification", fontsize=12, fontweight="bold")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.axis("off")
    plt.tight_layout()
    overlay_out = REPO_ROOT / "v&v" / "Abdou2021" / "Fig06_digitization_overlay.png"
    plt.savefig(overlay_out, dpi=250, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved Fig06 overlay to {overlay_out}")

if __name__ == "__main__":
    main()
