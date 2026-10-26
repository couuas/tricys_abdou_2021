#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""High-Fidelity Digitization of Abdou 2021 Figure 05.

Subject: Required TBR vs Availability Factor AF (%)
Curves:
- eta_f * fb = 0.5% (brown diamond, dotted)
- eta_f * fb = 1.0% (light blue triangle, solid, reference)
- eta_f * fb = 2.0% (red square, dashed)
- eta_f * fb = 3.0% (navy circle, dash-dot)
"""

from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
IMG_PATH = REPO_ROOT / "v&v" / "Abdou2021" / "Fig05.png"
OUT_DIR = REPO_ROOT / "v&v" / "data" / "track2" / "literature_markers"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Coordinate system
X_LEFT = 250.0
X_RIGHT = 1847.0
DX = (X_RIGHT - X_LEFT) / 100.0   # 15.97 px / %

Y_TOP = 20.0
Y_BOTTOM = 1397.0
DY = (Y_BOTTOM - Y_TOP) / 0.30     # 4590.0 px / unit TBR

def val_to_px(af, tbr):
    px = X_LEFT + af * DX
    py = Y_BOTTOM - (tbr - 1.00) * DY
    return px, py

def px_to_val(px, py):
    af = (px - X_LEFT) / DX
    tbr = 1.00 + (Y_BOTTOM - py) / DY
    return af, tbr

# Markers specifications:
# AF points: ~[6.5, 10.4, 18.9, 31.8, 50.0, 77.8, 100.0]%
curves_spec = [
    {
        "name": "eta_f_fb_0.5pct",
        "eta_f_fb_pct": 0.5,
        "symbol": "diamond",
        "color_filter": lambda rgb: float(rgb[0] - rgb[2]) if (rgb[0] > 110 and rgb[0] < 190 and rgb[1] > 80 and rgb[1] < 150 and rgb[2] < 100) else 0.0,
        "points": [
            (31.8, 1.295),
            (50.0, 1.213),
            (77.8, 1.195),
            (100.0, 1.185),
        ],
    },
    {
        "name": "eta_f_fb_1.0pct",
        "eta_f_fb_pct": 1.0,
        "symbol": "triangle",
        "color_filter": lambda rgb: float(rgb[2] - rgb[0]) if (rgb[2] > 150 and rgb[1] > 100 and rgb[0] < 140 and rgb[2] > rgb[1]) else 0.0,
        "points": [
            (18.9, 1.227),
            (31.8, 1.151),
            (50.0, 1.108),
            (77.8, 1.100),
            (100.0, 1.095),
        ],
    },
    {
        "name": "eta_f_fb_2.0pct",
        "eta_f_fb_pct": 2.0,
        "symbol": "square",
        "color_filter": lambda rgb: float(rgb[0] - max(rgb[1], rgb[2])) if (rgb[0] > 150 and rgb[1] < 100 and rgb[2] < 100) else 0.0,
        "points": [
            (10.4, 1.195),
            (18.9, 1.118),
            (31.8, 1.078),
            (50.0, 1.056),
            (77.8, 1.052),
            (100.0, 1.049),
        ],
    },
    {
        "name": "eta_f_fb_3.0pct",
        "eta_f_fb_pct": 3.0,
        "symbol": "circle",
        "color_filter": lambda rgb: float(rgb[2] - 0.5*(rgb[0]+rgb[1])) if (rgb[2] > 70 and rgb[2] < 160 and rgb[0] < 80 and rgb[1] < 80) else 0.0,
        "points": [
            (6.5, 1.208),
            (10.4, 1.134),
            (18.9, 1.081),
            (31.8, 1.054),
            (50.0, 1.039),
            (77.8, 1.035),
            (100.0, 1.033),
        ],
    },
]

def main():
    img = Image.open(IMG_PATH)
    arr = np.array(img, dtype=np.float32)

    rows = []
    win = 16

    for c in curves_spec:
        print(f"\nProcessing Fig05: {c['name']}")
        for af_nom, tbr_approx in c["points"]:
            px, py = val_to_px(af_nom, tbr_approx)
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

            det_af, det_tbr = px_to_val(cx, cy)
            row = {
                "figure": "Fig05",
                "curve": c["name"],
                "eta_f_fb_pct": c["eta_f_fb_pct"],
                "marker_symbol": c["symbol"],
                "AF_nominal_pct": round(float(af_nom), 2),
                "AF_detected_pct": round(float(det_af), 2),
                "required_tbr": round(float(det_tbr), 4),
                "pixel_x": round(float(cx), 2),
                "pixel_y": round(float(cy), 2),
            }
            rows.append(row)
            print(f"  AF={af_nom:5.1f}% -> det_AF={det_af:5.1f}%, TBR={det_tbr:.4f}")

    df = pd.DataFrame(rows)
    out_csv = OUT_DIR / "Fig05_literature_markers.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nSaved Fig05 markers ({len(df)} points) to {out_csv}")

    # Overlay plot
    fig, ax = plt.subplots(figsize=(10, 8), dpi=250)
    ax.imshow(img)
    cmap = {"eta_f_fb_0.5pct": "#FFD600", "eta_f_fb_1.0pct": "#00E5FF", "eta_f_fb_2.0pct": "#FF1744", "eta_f_fb_3.0pct": "#76FF03"}
    for c in curves_spec:
        sub = df[df["curve"] == c["name"]]
        ax.plot(sub["pixel_x"], sub["pixel_y"], color=cmap[c["name"]], lw=1.8, alpha=0.9, label=c["name"])
        ax.scatter(sub["pixel_x"], sub["pixel_y"], color="none", edgecolor=cmap[c["name"]], s=70, lw=2.0, zorder=5)

    ax.set_title("Abdou 2021 Fig 05: Discrete Markers Overlay Verification", fontsize=12, fontweight="bold")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.axis("off")
    plt.tight_layout()
    overlay_out = REPO_ROOT / "v&v" / "Abdou2021" / "Fig05_digitization_overlay.png"
    plt.savefig(overlay_out, dpi=250, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved Fig05 overlay to {overlay_out}")

if __name__ == "__main__":
    main()
