"""Group 3: Start-up inventory & global supply crisis (Figs 9, 10, 11, 12, 13, 15, 16).
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tricys.workflow.base import PluginMetadata, PostprocessPlugin
from tricys.workflow.context import PipelineContext
from tricys.workflow.registry import register_postprocess_plugin
from .common import load_benchmark_data

logger = logging.getLogger(__name__)


@register_postprocess_plugin("abdou_group3_startup_inventory")
class AbdouGroup3Plugin(PostprocessPlugin):
    """Postprocessing plugin for Abdou 2021 Group 3 benchmarks (Start-up inventory & external supply)."""

    name = "abdou_group3_startup_inventory"

    @classmethod
    def get_metadata(cls) -> PluginMetadata:
        return PluginMetadata(
            name=cls.name,
            category="postprocess",
            description="Abdou 2021 Group 3: Start-up inventory collapse, reserve time & 2000-2060 global supply window.",
            version="2.0.0",
            author="TRICYS V&V Team",
            parameters_schema={
                "dpi": {"type": "integer", "default": 300},
                "output_dir": {"type": "string", "default": ""},
            },
            input_requirements=[],
            output_artifacts=[
                "Fig09_global_tritium_supply_2000_2060.png",
                "Fig10_startup_inventory_vs_burnup.png",
                "Fig11_startup_inventory_vs_dir.png",
                "Fig12_startup_inventory_vs_reserve_time.png",
                "Fig13_reserve_inventory_vs_reserve_time.png",
                "Fig15_startup_inventory_vs_power.png",
                "Fig16_reactor_comparison_startup.png",
                "group3_startup_inventory_data.csv",
            ],
        )

    def validate(self, context: PipelineContext) -> bool:
        return True

    def run(self, context: PipelineContext) -> None:
        out_dir = Path(self.params.get("output_dir") or context.results_dir or "./results")
        fig_dir = out_dir / "figures" if (out_dir / "figures").exists() else out_dir
        data_dir = out_dir / "data" if (out_dir / "data").exists() else out_dir
        fig_dir.mkdir(parents=True, exist_ok=True)
        data_dir.mkdir(parents=True, exist_ok=True)
        dpi = int(self.params.get("dpi", 300))

        logger.info(f"[{self.name}] Generating Group 3 publication figures & inventory data...")

        self._plot_figure_9(context, fig_dir / "Fig09_global_tritium_supply_2000_2060.png", dpi)
        self._plot_figure_10(context, fig_dir / "Fig10_startup_inventory_vs_burnup.png", dpi)
        self._plot_figure_11(context, fig_dir / "Fig11_startup_inventory_vs_dir.png", dpi)
        self._plot_figure_12(context, fig_dir / "Fig12_startup_inventory_vs_reserve_time.png", dpi)
        self._plot_figure_13(context, fig_dir / "Fig13_reserve_inventory_vs_reserve_time.png", dpi)
        self._plot_figure_15(context, fig_dir / "Fig15_startup_inventory_vs_power.png", dpi)
        self._plot_figure_16(context, fig_dir / "Fig16_reactor_comparison_startup.png", dpi)
        self._export_group3_data(data_dir / "group3_startup_inventory_data.csv", context)

        logger.info(f"[{self.name}] Group 3 completed successfully.")

    def _plot_figure_9(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        df = load_benchmark_data(context, "Fig09_global_tritium_supply", ["group3_fig09_global_supply.csv"])
        fig, ax = plt.subplots(figsize=(8.5, 6), dpi=dpi)

        years = df["year"]
        ax.plot(years, df["total_candu_available_kg"], color="#1565C0", lw=2.5, label="Total Global Non-Military Supply (CANDU)")
        ax.plot(years, df["net_after_iter_kg"], color="#D32F2F", lw=2.2, linestyle="--", label="Net Available After ITER Consumption")

        ax.axhline(5.0, color="#7B1FA2", linestyle=":", lw=1.5, label="DEMO Min Startup Threshold (5 kg)")
        peak_idx = df["total_candu_available_kg"].idxmax()
        peak_yr = df.loc[peak_idx, "year"]
        peak_val = df.loc[peak_idx, "total_candu_available_kg"]

        ax.scatter([peak_yr], [peak_val], color="#D50000", s=60, zorder=5)

        ax.set_xlim(2000, 2060)
        ax.set_ylim(0, 32)
        ax.set_xlabel("Year (2000 - 2060)", fontsize=11, fontweight="bold")
        ax.set_ylabel("Available Tritium Inventory (kg)", fontsize=11, fontweight="bold")
        ax.set_title("Abdou 2021 Figure 9: Global Commercial Tritium Inventory Evolution Window",
                     fontsize=12, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(frameon=True, loc="upper right")
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_10(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        df = load_benchmark_data(context, "Fig10_startup_inventory_vs_burnup", [
            "group3_fig10_startup_inventory_real.csv",
            "Fig10_startup_inventory_vs_burnup.csv",
            "Fig10_required_tbr_summary.csv",
            "required_tbr_summary.csv"
        ])
        if "startup_inventory_IS0_kg" not in df.columns:
            if "I_S_0" in df.columns:
                df["startup_inventory_IS0_kg"] = df["I_S_0"] / 1000.0
            elif "startup_inventory" in df.columns:
                df["startup_inventory_IS0_kg"] = df["startup_inventory"] / 1000.0
        if "core_product_pct" not in df.columns and "f_b" in df.columns and "eta_f" in df.columns:
            df["core_product_pct"] = (df["f_b"] * df["eta_f"] * 100.0).round(2)
        if "tp_hours" not in df.columns:
            if "name" in df.columns:
                df["tp_hours"] = df["name"].apply(
                    lambda n: 1.0 if "tp1h" in str(n) else (12.0 if "tp12h" in str(n) else (4.0 if "tp4h" in str(n) else np.nan))
                )
            elif "case_name" in df.columns:
                df["tp_hours"] = df["case_name"].apply(
                    lambda n: 1.0 if "tp1h" in str(n) else (12.0 if "tp12h" in str(n) else (4.0 if "tp4h" in str(n) else np.nan))
                )
            if "tp_hours" not in df.columns or df["tp_hours"].isna().any():
                if "comp9_ISS.tau_9" in df.columns:
                    tau9 = df["comp9_ISS.tau_9"].fillna(3.5)
                    calc_tp = tau9.apply(lambda t: 1.0 if t < 1.0 else (12.0 if t > 6.0 else 4.0))
                    df["tp_hours"] = df["tp_hours"].fillna(calc_tp) if "tp_hours" in df.columns else calc_tp
                else:
                    df["tp_hours"] = df["tp_hours"].fillna(4.0) if "tp_hours" in df.columns else 4.0

        fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=dpi)

        curves = [
            (1.0, "#2E7D32", "o", "-", r"$t_p = 1$ h"),
            (4.0, "#D32F2F", "s", "--", r"$t_p = 4$ h (Reference)"),
            (12.0, "#0D47A1", "^", "-.", r"$t_p = 12$ h"),
        ]
        for tp, col, m, ls, lbl in curves:
            sub = df[df["tp_hours"] == tp].sort_values("core_product_pct")
            sub_plot = sub[sub["core_product_pct"] >= 0.5]
            if not sub_plot.empty:
                ax.plot(sub_plot["core_product_pct"], sub_plot["startup_inventory_IS0_kg"],
                        color=col, marker=m, ls=ls, lw=2.2, ms=6, label=lbl)

        ax.axhline(5.0, color="#7B1FA2", ls="--", lw=1.5, label="External Supply Ceiling (~5 kg)")
        ax.axvspan(2.0, 5.0, color="#C8E6C9", alpha=0.3, label=r"Commercial Safe Window ($\geq 2.0\%$)")

        ax.set_xlim(0.3, 5.2)
        ax.set_ylim(0, 55)
        ax.set_xlabel(r"Core Product $\eta_f f_b$ (%)", fontweight="bold", fontsize=11)
        ax.set_ylabel(r"Start-up Tritium Inventory $I_S^0$ (kg)", fontweight="bold", fontsize=11)
        ax.set_title("Abdou 2021 Figure 10: Start-up Inventory Collapse vs Core Product",
                     fontsize=12, fontweight="bold")
        ax.grid(True, ls=":", alpha=0.6)
        ax.legend(loc="upper right", fontsize=8.5)
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_11(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        df = load_benchmark_data(context, "Fig11_startup_inventory_vs_dir", [
            "group3_fig11_startup_inventory_vs_dir_real.csv",
            "group2_fig06_dir_sweep_real.csv",
            "Fig11_startup_inventory_vs_dir.csv",
            "Fig11_required_tbr_summary.csv",
            "required_tbr_summary.csv"
        ])
        if "startup_inventory_IS0_kg" not in df.columns:
            if "I_S_0" in df.columns:
                df["startup_inventory_IS0_kg"] = df["I_S_0"] / 1000.0
            elif "startup_inventory" in df.columns:
                df["startup_inventory_IS0_kg"] = df["startup_inventory"] / 1000.0
        if "dir_fraction_pct" not in df.columns:
            for k in ["f_DIR", "tep.DIR", "DIR", "f_dir", "dir"]:
                if k in df.columns:
                    df["dir_fraction_pct"] = (df[k] * 100.0).round(1)
                    break
        if "core_product_pct" not in df.columns and "f_b" in df.columns and "eta_f" in df.columns:
            df["core_product_pct"] = (df["f_b"] * df["eta_f"] * 100.0).round(2)

        fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=dpi)

        curves = [
            (0.5, "#2E7D32", "D", ":", r"$\eta_f f_b = 0.5\%$"),
            (1.0, "#D32F2F", "s", "--", r"$\eta_f f_b = 1.0\%$ (Reference)"),
            (2.0, "#0D47A1", "o", "-", r"$\eta_f f_b = 2.0\%$"),
            (3.0, "#C2185B", "P", "-.", r"$\eta_f f_b = 3.0\%$"),
        ]
        for prod_pct, col, m, ls, lbl in curves:
            sub = df[np.isclose(df["core_product_pct"], prod_pct, atol=0.05)].sort_values("dir_fraction_pct")
            if not sub.empty:
                sub_plot = sub[sub["dir_fraction_pct"] >= 10.0]
                ax.plot(sub_plot["dir_fraction_pct"], sub_plot["startup_inventory_IS0_kg"],
                        color=col, marker=m, ls=ls, lw=2.2, ms=6, label=lbl)

        ax.axhline(5.0, color="#7B1FA2", ls="--", lw=1.5, label="External Supply Ceiling (~5 kg)")
        ax.set_xlim(8, 92)
        ax.set_ylim(0, 60)
        ax.set_xlabel("Direct Internal Recycling (DIR) Fraction (%)", fontweight="bold", fontsize=11)
        ax.set_ylabel(r"Start-up Inventory $I_S^0$ (kg)", fontweight="bold", fontsize=11)
        ax.set_title("Abdou 2021 Figure 11: Start-up Inventory Reduction via Direct Internal Recycling",
                     fontsize=12, fontweight="bold")
        ax.grid(True, ls=":", alpha=0.6)
        ax.legend(loc="upper right", fontsize=8.5)
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_12(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        df = load_benchmark_data(context, "Fig12_startup_inventory_vs_reserve_time", [
            "group3_fig12_14_reserve_time.csv",
            "Fig12_startup_inventory_vs_reserve_time.csv",
            "Fig12_required_tbr_summary.csv",
            "required_tbr_summary.csv"
        ])
        if "startup_inventory_IS0_kg" not in df.columns:
            if "I_S_0" in df.columns:
                df["startup_inventory_IS0_kg"] = df["I_S_0"] / 1000.0
            elif "startup_inventory" in df.columns:
                df["startup_inventory_IS0_kg"] = df["startup_inventory"] / 1000.0
        if "core_product_pct" not in df.columns and "f_b" in df.columns and "eta_f" in df.columns:
            df["core_product_pct"] = (df["f_b"] * df["eta_f"] * 100.0).round(2)
        tr_col = "t_r" if "t_r" in df.columns else "reserve_time_tr_hours"

        fig, ax = plt.subplots(figsize=(8.5, 6), dpi=dpi)

        prods = [
            (0.5, r"$\eta_f f_b = 0.5\%$", "#D32F2F", "-"),
            (1.0, r"$\eta_f f_b = 1.0\%$", "#EF6C00", "--"),
            (2.0, r"$\eta_f f_b = 2.0\%$", "#2E7D32", "-."),
            (5.0, r"$\eta_f f_b = 5.0\%$", "#1565C0", ":"),
        ]
        for prod_pct, label, color, ls in prods:
            sub = df[np.isclose(df["core_product_pct"], prod_pct, atol=0.05)].sort_values(tr_col)
            if not sub.empty:
                ax.plot(sub[tr_col], sub["startup_inventory_IS0_kg"],
                        label=label, color=color, linestyle=ls, lw=2.2)

        ax.axhline(5.0, color="#7B1FA2", linestyle="--", lw=1.5, label="Supply Ceiling (~5 kg)")
        ax.set_xlim(0, 48)
        ax.set_ylim(0, 50)
        ax.set_xlabel("Reserve Time $t_r$ (hours)", fontsize=11, fontweight="bold")
        ax.set_ylabel(r"Start-up Inventory $I_S^0$ (kg)", fontsize=11, fontweight="bold")
        ax.set_title("Abdou 2021 Figure 12: Start-up Inventory vs Reserve Time", fontsize=12, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(frameon=True, loc="upper left")
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_13(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        df = load_benchmark_data(context, "Fig13_reserve_inventory_vs_reserve_time", ["Fig13_reserve_inventory_vs_reserve_time.csv", "group3_fig12_14_reserve_time.csv"])
        if "core_product_pct" not in df.columns and "f_b" in df.columns and "eta_f" in df.columns:
            df["core_product_pct"] = (df["f_b"] * df["eta_f"] * 100.0).round(2)
        if "I_r_kg" not in df.columns:
            if "I_reserve_req" in df.columns:
                df["I_r_kg"] = df["I_reserve_req"] / 1000.0
            elif "comp11_Storage.I_reserve_req" in df.columns:
                df["I_r_kg"] = df["comp11_Storage.I_reserve_req"] / 1000.0
            elif "f_b" in df.columns and "eta_f" in df.columns and "t_r" in df.columns:
                p_fus = df["P_fus"] if "P_fus" in df.columns else 3000.0
                q_fail = df["q_fail"] if "q_fail" in df.columns else 0.25
                n_dot = 19.125 * (p_fus / 3000.0)
                df["I_r_kg"] = ((n_dot / (df["eta_f"] * df["f_b"])) * df["t_r"] * q_fail) / 1000.0

        fig, ax = plt.subplots(figsize=(8.5, 6), dpi=dpi)

        prods = [
            (0.5, r"$\eta_f f_b = 0.5\%$", "#D32F2F", "-"),
            (1.0, r"$\eta_f f_b = 1.0\%$", "#EF6C00", "--"),
            (2.0, r"$\eta_f f_b = 2.0\%$", "#2E7D32", "-."),
            (5.0, r"$\eta_f f_b = 5.0\%$", "#1565C0", ":"),
        ]
        tr_col = "t_r" if "t_r" in df.columns else "reserve_time_tr_hours"
        ir_col = "I_r_kg" if "I_r_kg" in df.columns else "reserve_inventory_Ir_kg"

        for prod_pct, label, color, ls in prods:
            sub = df[np.isclose(df["core_product_pct"], prod_pct, atol=0.05)].sort_values(tr_col)
            if not sub.empty:
                ax.plot(sub[tr_col], sub[ir_col], label=label, color=color, linestyle=ls, lw=2.2)

        ax.set_xlim(0, 48)
        ax.set_ylim(0, 50)
        ax.set_xlabel("Reserve Time $t_r$ (hours)", fontsize=11, fontweight="bold")
        ax.set_ylabel(r"Reserve Inventory $I_r$ (kg)", fontsize=11, fontweight="bold")
        ax.set_title("Abdou 2021 Figure 13: Reserve Inventory vs Reserve Time", fontsize=12, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(frameon=True, loc="upper left")
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_15(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        df = load_benchmark_data(context, "Fig15_startup_inventory_vs_power", [
            "group3_fig15_startup_inventory_vs_power_real.csv",
            "Fig15_startup_inventory_vs_power.csv",
            "Fig15_required_tbr_summary.csv",
            "required_tbr_summary.csv"
        ])
        if "fusion_power_MW" not in df.columns and "P_fus" in df.columns:
            df["fusion_power_MW"] = df["P_fus"]
        if "core_product" not in df.columns and "f_b" in df.columns and "eta_f" in df.columns:
            df["core_product"] = (df["f_b"] * df["eta_f"]).round(4)
        if "startup_inventory_IS0_kg" not in df.columns and "I_S_0" in df.columns:
            df["startup_inventory_IS0_kg"] = df["I_S_0"] / 1000.0

        fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=dpi)

        curves = [
            (0.005, 24.0, "startup_inventory_tr24h_kg", "#D32F2F", "o", "-", r"$\eta_f f_b = 0.5\%,\ t_r = 24$ h"),
            (0.005, 6.0,  "startup_inventory_tr6h_kg",  "#E64A19", "s", "--", r"$\eta_f f_b = 0.5\%,\ t_r = 6$ h"),
            (0.050, 24.0, "startup_inventory_tr24h_kg", "#0D47A1", "^", "-.", r"$\eta_f f_b = 5.0\%,\ t_r = 24$ h"),
            (0.050, 6.0,  "startup_inventory_tr6h_kg",  "#1976D2", "d", ":",  r"$\eta_f f_b = 5.0\%,\ t_r = 6$ h"),
        ]
        has_tr = "t_r" in df.columns
        for prod, tr_val, col_name, color, marker, ls, lbl in curves:
            if has_tr:
                sub = df[np.isclose(df["core_product"], prod, atol=0.001) & np.isclose(df["t_r"], tr_val, atol=0.5)].sort_values("fusion_power_MW")
                y_col = "startup_inventory_IS0_kg" if "startup_inventory_IS0_kg" in sub.columns else col_name
            else:
                sub = df[np.isclose(df["core_product"], prod, atol=0.001)].sort_values("fusion_power_MW")
                y_col = col_name

            if not sub.empty and y_col in sub.columns:
                ax.plot(sub["fusion_power_MW"], sub[y_col],
                        color=color, marker=marker, ls=ls, lw=2.2, ms=6, label=lbl)

        ax.axhline(5.0, color="#7B1FA2", ls="--", lw=1.5, label="External Supply Ceiling (~5 kg)")
        ax.set_xlim(50, 3050)
        ax.set_ylim(0, 35)
        ax.set_xlabel("Fusion Power (MW)", fontweight="bold", fontsize=11)
        ax.set_ylabel(r"Start-up Inventory $I_S^0$ (kg)", fontweight="bold", fontsize=11)
        ax.set_title(r"Abdou 2021 Figure 15: Start-up Inventory Linear Scaling with Fusion Power",
                     fontsize=11.5, fontweight="bold")
        ax.grid(True, ls=":", alpha=0.6)
        ax.legend(loc="upper left", fontsize=8.5)
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_16(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        df = load_benchmark_data(context, "Fig16_reactor_comparison_startup", ["group3_fig16_reactor_comparison.csv"])
        fig, ax = plt.subplots(figsize=(9, 6), dpi=dpi)

        reactors = df["reactor_concept"].tolist()
        i_s0_1pct = df["startup_inventory_target_1pct_kg"].tolist()
        i_s0_3pct = df["startup_inventory_advanced_3pct_kg"].tolist()

        x = np.arange(len(reactors))
        width = 0.35

        ax.bar(x - width/2, i_s0_1pct, width, label=r"Target $\eta_f f_b = 1.0\%$", color="#1565C0", alpha=0.85)
        ax.bar(x + width/2, i_s0_3pct, width, label=r"Advanced $\eta_f f_b = 3.0\%$", color="#2E7D32", alpha=0.85)

        ax.axhline(5.0, color="#D32F2F", linestyle="--", lw=1.8, label="Global Available Supply Ceiling (~5 kg)")
        ax.set_ylabel(r"Start-up Tritium Inventory $I_S^0$ (kg)", fontsize=11, fontweight="bold")
        ax.set_title("Abdou 2021 Figure 16: Start-up Inventory Comparison Across Fusion Reactor Concepts",
                     fontsize=12, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(reactors, fontsize=10, fontweight="semibold")
        ax.grid(True, axis="y", linestyle="--", alpha=0.5)
        ax.legend(frameon=True, loc="upper left")
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _export_group3_data(self, csv_path: Path, context: PipelineContext) -> None:
        try:
            df = load_benchmark_data(context, "group3_export", ["group3_fig15_startup_inventory_vs_power_real.csv"])
            df.to_csv(csv_path, index=False)
            context.artifacts["group3_startup_inventory_data"] = str(csv_path)
        except Exception as e:
            logger.warning(f"Could not export group3 data: {e}")
