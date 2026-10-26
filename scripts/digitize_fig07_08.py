#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""High-Fidelity Digitization of Abdou 2021 Figure 07 and Figure 08.

Fig07: Near-Term FNSF Required TBR vs Core Product (AF = 30%)
Fig08: Commercial Required TBR vs Core Product (AF = 80%)
Curves:
- td = 1 yr (light blue circle, dotted)
- td = 3 yr (red square, dashed)
- td = 5 yr (light purple triangle, dash-dot)
- td = 7 yr (dark navy star, solid)
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

def digitize_fig(fig_name, x_box, y_box, y_max, curves_spec):
    img_path = IMG_DIR / f"{fig_name}.png"
    img = Image.open(img_path)
    arr = np.array(img, dtype=np.float32)

    x_left, x_right = x_box
    y_top, y_bottom = y_box
    dx = (x_right - x_left) / 5.0
    dy = (y_bottom - y_top) / (y_max - 1.00)

    def val_to_px(x, y):
        return x_left + x * dx, y_bottom - (y - 1.00) * dy

    def px_to_val(px, py):
        return (px - x_left) / dx, 1.00 + (y_bottom - py) / dy

    rows = []
    win = 16

    print(f"\n==================== Processing {fig_name} ====================")
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
                "figure": fig_name,
                "curve": c["name"],
                "td_years": c["td_years"],
                "marker_symbol": c["symbol"],
                "eta_f_fb_nominal_pct": round(float(x_nom), 2),
                "eta_f_fb_detected_pct": round(float(det_x), 3),
                "required_tbr": round(float(det_y), 4),
                "pixel_x": round(float(cx), 2),
                "pixel_y": round(float(cy), 2),
            }
            rows.append(row)
            print(f"  x={x_nom:4.2f}% -> det_x={det_x:5.3f}%, TBR={det_y:.4f}")

    df = pd.DataFrame(rows)
    out_csv = OUT_DIR / f"{fig_name}_literature_markers.csv"
    df.to_csv(out_csv, index=False)
    print(f"Saved {fig_name} markers ({len(df)} points) to {out_csv}")

    # Overlay
    fig, ax = plt.subplots(figsize=(10, 8), dpi=250)
    ax.imshow(img)
    cmap = {"td_1yr": "#00E5FF", "td_3yr": "#FF1744", "td_5yr": "#E040FB", "td_7yr": "#76FF03"}
    for c in curves_spec:
        sub = df[df["curve"] == c["name"]]
        ax.plot(sub["pixel_x"], sub["pixel_y"], color=cmap[c["name"]], lw=1.8, alpha=0.9, label=c["name"])
        ax.scatter(sub["pixel_x"], sub["pixel_y"], color="none", edgecolor=cmap[c["name"]], s=70, lw=2.0, zorder=5)

    ax.set_title(f"Abdou 2021 {fig_name}: Discrete Markers Overlay Verification", fontsize=12, fontweight="bold")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.axis("off")
    plt.tight_layout()
    overlay_out = IMG_DIR / f"{fig_name}_digitization_overlay.png"
    plt.savefig(overlay_out, dpi=250, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {fig_name} overlay to {overlay_out}")

# Color filters
# Light blue circle (td=1yr): B > R+40, G > 100, R < 140
blue_f = lambda rgb: float(rgb[2] - rgb[0]) if (rgb[2] > 140 and rgb[1] > 100 and rgb[0] < 140 and rgb[2] > rgb[1]) else 0.0
# Red square (td=3yr): R > G+40, R > B+40
red_f = lambda rgb: float(rgb[0] - max(rgb[1], rgb[2])) if (rgb[0] > 140 and rgb[1] < 100 and rgb[2] < 100) else 0.0
# Light purple triangle (td=5yr): R ~ 180-210, G ~ 160-190, B ~ 190-220 (pale purple/slate)
purple_f = lambda rgb: float(rgb[2] - rgb[1]) if (rgb[2] > 160 and rgb[0] > 150 and rgb[1] > 130 and rgb[2] > rgb[1]+10) else 0.0
# Dark navy star (td=7yr): very dark blue, R < 70, G < 70, B in [60, 140], B > R+15
navy_f = lambda rgb: float(rgb[2] - 0.5*(rgb[0]+rgb[1])) if (rgb[2] > 60 and rgb[2] < 150 and rgb[0] < 70 and rgb[1] < 70) else 0.0

def main():
    # Fig07 (AF = 30%)
    fig07_curves = [
        {"name": "td_1yr", "td_years": 1.0, "symbol": "circle", "color_filter": blue_f,
         "points": [(2.0, 1.278), (3.0, 1.236), (4.0, 1.186), (5.0, 1.156)]},
        {"name": "td_3yr", "td_years": 3.0, "symbol": "square", "color_filter": red_f,
         "points": [(0.8, 1.252), (1.0, 1.205), (1.5, 1.137), (2.0, 1.106), (2.5, 1.086), (3.0, 1.073), (4.0, 1.057), (5.0, 1.047)]},
        {"name": "td_5yr", "td_years": 5.0, "symbol": "triangle", "color_filter": purple_f,
         "points": [(0.8, 1.196), (1.0, 1.157), (1.5, 1.111), (2.0, 1.084), (2.5, 1.069), (3.0, 1.058), (4.0, 1.045), (5.0, 1.037)]},
        {"name": "td_7yr", "td_years": 7.0, "symbol": "star", "color_filter": navy_f,
         "points": [(0.5, 1.294), (0.8, 1.184), (1.0, 1.149), (1.5, 1.102), (2.0, 1.077), (2.5, 1.063), (3.0, 1.053), (4.0, 1.042), (5.0, 1.034)]},
    ]
    digitize_fig("Fig07", (325.0, 1872.0), (25.0, 1302.0), 1.30, fig07_curves)

    # Fig08 (AF = 80%)
    fig08_curves = [
        {"name": "td_1yr", "td_years": 1.0, "symbol": "circle", "color_filter": blue_f,
         "points": [(1.5, 1.203), (2.0, 1.155), (2.5, 1.128), (3.0, 1.110), (4.0, 1.085), (5.0, 1.072)]},
        {"name": "td_3yr", "td_years": 3.0, "symbol": "square", "color_filter": red_f,
         "points": [(0.8, 1.161), (1.0, 1.131), (1.5, 1.089), (2.0, 1.069), (2.5, 1.056), (3.0, 1.048), (4.0, 1.037), (5.0, 1.031)]},
        {"name": "td_5yr", "td_years": 5.0, "symbol": "triangle", "color_filter": purple_f,
         "points": [(0.5, 1.171), (0.8, 1.109), (1.0, 1.088), (1.5, 1.060), (2.0, 1.046), (2.5, 1.038), (3.0, 1.032), (4.0, 1.025), (5.0, 1.021)]},
        {"name": "td_7yr", "td_years": 7.0, "symbol": "star", "color_filter": navy_f,
         "points": [(0.5, 1.140), (0.8, 1.088), (1.0, 1.071), (1.5, 1.049), (2.0, 1.038), (2.5, 1.031), (3.0, 1.026), (4.0, 1.021), (5.0, 1.018)]},
    ]
    digitize_fig("Fig08", (324.0, 1861.0), (28.0, 1295.0), 1.25, fig08_curves)

if __name__ == "__main__":
    main()
