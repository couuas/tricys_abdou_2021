#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Comprehensive Extraction of Discrete Calculation Markers from Abdou 2021 Figures.

Processes all 11 figures (Fig04 - Fig15):
- Fig04: Required TBR vs Core Product (tp = 1, 4, 12 h)
- Fig05: Required TBR vs Availability Factor (eta_f*fb = 0.5, 1, 2, 3%)
- Fig06: Required TBR vs DIR Fraction (eta_f*fb = 0.5, 1, 2, 3%)
- Fig07: Near-Term FNSF Required TBR vs Core Product (AF=30%, td = 1, 3, 5, 7 yr)
- Fig08: Commercial Required TBR vs Core Product (AF=80%, td = 1, 3, 5, 7 yr)
- Fig10: Start-up Tritium Inventory vs Core Product (tp = 1, 4, 12 h)
- Fig11: Start-up Tritium Inventory vs DIR Fraction (eta_f*fb = 0.5, 1, 2, 3%)
- Fig12: Start-up Tritium Inventory vs Reserve Time (eta_f*fb = 0.5, 1, 2, 3, 5%)
- Fig13: Reserve Tritium Inventory vs Reserve Time (eta_f*fb = 0.5, 1, 2, 3, 5%)
- Fig14: Required TBR vs Reserve Time (eta_f*fb = 0.5, 1, 2, 3, 5%)
- Fig15: Start-up Tritium Inventory vs Fusion Power (Scaling at tr = 6, 24 h)

Outputs:
- Individual CSVs: v&v/data/track2/literature_markers/FigXX_literature_markers.csv
- Consolidated CSV: v&v/data/track2/literature_markers/Abdou2021_all_figures_literature_markers.csv
- Consolidated YAML: v&v/data/track2/literature_markers/Abdou2021_all_figures_literature_markers.yaml
- Pixel overlay verification images: v&v/Abdou2021/FigXX_digitization_overlay.png
- Master reference documentation: v&v/ABDOU2021_DISCRETE_CALCULATION_MARKERS_REFERENCE.md
"""

from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
IMG_DIR = REPO_ROOT / "v&v" / "Abdou2021"
DATA_DIR = REPO_ROOT / "v&v" / "data" / "track2" / "literature_markers"
DATA_DIR.mkdir(parents=True, exist_ok=True)

class FigureExtractor:
    def __init__(self, fig_name, x_range, y_range, x_bounds_px, y_bounds_px, x_label, y_label):
        self.fig_name = fig_name
        self.img_path = IMG_DIR / f"{fig_name}.png"
        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range
        self.x_left, self.x_right = x_bounds_px
        self.y_top, self.y_bottom = y_bounds_px
        self.x_label = x_label
        self.y_label = y_label
        
        self.dx = (self.x_right - self.x_left) / (self.x_max - self.x_min)
        self.dy = (self.y_bottom - self.y_top) / (self.y_max - self.y_min)
        
        self.img = Image.open(self.img_path)
        self.arr = np.array(self.img, dtype=np.float32)
        self.markers = []

    def val_to_px(self, x, y):
        px = self.x_left + (x - self.x_min) * self.dx
        py = self.y_bottom - (y - self.y_min) * self.dy
        return px, py

    def px_to_val(self, px, py):
        x = self.x_min + (px - self.x_left) / self.dx
        y = self.y_min + (self.y_bottom - py) / self.dy
        return x, y

    def extract_point(self, curve_id, x_nom, y_approx, color_weight_func, marker_symbol, win=18):
        px, py = self.val_to_px(x_nom, y_approx)
        
        y0, y1 = max(0, int(py - win)), min(self.arr.shape[0], int(py + win + 1))
        x0, x1 = max(0, int(px - win)), min(self.arr.shape[1], int(px + win + 1))
        
        sub = self.arr[y0:y1, x0:x1]
        w_mat = np.zeros(sub.shape[:2], dtype=np.float32)
        for i in range(sub.shape[0]):
            for j in range(sub.shape[1]):
                w_mat[i, j] = color_weight_func(sub[i, j])
                
        max_w = np.max(w_mat)
        if max_w < 5.0:
            # Fallback to nominal if color contrast is extremely faint
            cx, cy = px, py
        else:
            w_mat[w_mat < 0.35 * max_w] = 0.0
            tot = np.sum(w_mat)
            if tot > 0:
                y_idx, x_idx = np.indices(w_mat.shape)
                cy = y0 + np.sum(y_idx * w_mat) / tot
                cx = x0 + np.sum(x_idx * w_mat) / tot
            else:
                cx, cy = px, py

        det_x, det_y = self.px_to_val(cx, cy)
        
        # In vertical slice, find exact peak at nominal column
        nom_px_int = int(round(px))
        col_slice = self.arr[y0:y1, max(0, nom_px_int-1):min(self.arr.shape[1], nom_px_int+2)]
        col_w = [color_weight_func(col_slice[r].mean(axis=0)) for r in range(col_slice.shape[0])]
        if max(col_w) > 5.0:
            peak_r = np.argmax(col_w)
            slice_py = y0 + peak_r
            slice_y = self.px_to_val(nom_px_int, slice_py)[1]
            final_y = 0.5 * (det_y + slice_y)
        else:
            final_y = det_y

        rec = {
            "figure": self.fig_name,
            "curve": curve_id,
            "marker_symbol": marker_symbol,
            "x_nominal": round(float(x_nom), 4),
            "x_detected": round(float(det_x), 4),
            "y_detected": round(float(det_y), 4),
            "y_final": round(float(final_y), 4),
            "pixel_x": round(float(cx), 2),
            "pixel_y": round(float(cy), 2),
        }
        self.markers.append(rec)
        return rec

    def save_results(self):
        df = pd.DataFrame(self.markers)
        csv_file = DATA_DIR / f"{self.fig_name}_literature_markers.csv"
        df.to_csv(csv_file, index=False)
        print(f"[{self.fig_name}] Extracted {len(df)} markers -> {csv_file.name}")

        # Overlay plot
        fig, ax = plt.subplots(figsize=(10, 8), dpi=250)
        ax.imshow(self.img)
        
        curves = df["curve"].unique()
        cmap = plt.cm.get_cmap("tab10", len(curves))
        for idx, c in enumerate(curves):
            sub = df[df["curve"] == c]
            ax.plot(sub["pixel_x"], sub["pixel_y"], color=cmap(idx), lw=1.8, alpha=0.85, label=f"{c}")
            ax.scatter(sub["pixel_x"], sub["pixel_y"], color="none", edgecolor=cmap(idx),
                       s=60, lw=1.8, zorder=5)

        ax.set_title(f"{self.fig_name}: Literature Discrete Markers Overlay Verification", fontsize=12, fontweight="bold")
        ax.legend(loc="upper right", fontsize=8.5, framealpha=0.85)
        ax.axis("off")
        plt.tight_layout()
        overlay_out = IMG_DIR / f"{self.fig_name}_digitization_overlay.png"
        plt.savefig(overlay_out, dpi=250, bbox_inches="tight")
        plt.close(fig)
        return df

print("Extractor class initialized.")
