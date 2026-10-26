"""Group 2: Tritium self-sufficiency & required TBR sweeps (Figs 4, 5, 6, 7, 8, 14, 17).
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


@register_postprocess_plugin("abdou_group2_self_sufficiency")
class AbdouGroup2Plugin(PostprocessPlugin):
    """Postprocessing plugin for Abdou 2021 Group 2 benchmarks (Required TBR phase space)."""

    name = "abdou_group2_self_sufficiency"

    @classmethod
    def get_metadata(cls) -> PluginMetadata:
        return PluginMetadata(
            name=cls.name,
            category="postprocess",
            description="Abdou 2021 Group 2: Required TBR sweeps across availability, core product, DIR & doubling time.",
            version="2.0.0",
            author="TRICYS V&V Team",
            parameters_schema={
                "dpi": {"type": "integer", "default": 300},
                "output_dir": {"type": "string", "default": ""},
            },
            input_requirements=[],
            output_artifacts=[
                "Fig04_tbr_vs_burnup.png",
                "Fig05_tbr_vs_availability.png",
                "Fig06_tbr_vs_dir.png",
                "Fig07_tbr_vs_doubling_time_4h.png",
                "Fig08_tbr_vs_doubling_time_1h.png",
                "Fig14_tbr_vs_reserve_time.png",
                "Fig17_fnsf_tbr_scenarios.png",
                "group2_self_sufficiency_data.csv",
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

        logger.info(f"[{self.name}] Generating Group 2 publication figures & sensitivity data...")

        self._plot_figure_4(context, fig_dir / "Fig04_tbr_vs_burnup.png", dpi)
        self._plot_figure_5(context, fig_dir / "Fig05_tbr_vs_availability.png", dpi)
        self._plot_figure_6(context, fig_dir / "Fig06_tbr_vs_dir.png", dpi)
        self._plot_figure_7(context, fig_dir / "Fig07_tbr_vs_doubling_time_4h.png", dpi)
        self._plot_figure_8(context, fig_dir / "Fig08_tbr_vs_doubling_time_1h.png", dpi)
        self._plot_figure_14(context, fig_dir / "Fig14_tbr_vs_reserve_time.png", dpi)
        self._plot_figure_17(context, fig_dir / "Fig17_fnsf_tbr_scenarios.png", dpi)
        self._export_group2_data(data_dir / "group2_self_sufficiency_data.csv", context)

        logger.info(f"[{self.name}] Group 2 completed successfully.")

    def _plot_figure_4(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        df = load_benchmark_data(context, "Fig04_tbr_vs_burnup", [
            "Fig04_required_tbr_summary.csv",
            "Fig04_tbr_vs_burnup.csv",
            "group2_fig04_tbr_vs_burnup_real.csv",
            "required_tbr_summary.csv"
        ])
        if "required_tbr" not in df.columns and "Required_TBR" in df.columns:
            df["required_tbr"] = df["Required_TBR"]
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

        ax.axhspan(1.00, 1.05, color="#A5D6A7", alpha=0.45, label=r"Attained with High Confidence ($\mathrm{TBR}_R \leq 1.05$)")
        ax.axhspan(1.05, 1.15, color="#C8E6C9", alpha=0.35, label=r"Possible Self-Sufficiency Window ($1.05 < \mathrm{TBR}_R \leq 1.15$)")
        ax.axhline(1.15, color="#2E7D32", ls="--", lw=1.2)
        ax.axhline(1.05, color="#1B5E20", ls=":", lw=1.2)

        curves = [
            (1.0, "#1E88E5", "o", "-", r"$t_p = 1$ h"),
            (4.0, "#D32F2F", "s", "--", r"$t_p = 4$ h (Reference)"),
            (12.0, "#0D47A1", "^", "-.", r"$t_p = 12$ h"),
        ]
        for tp, col, m, ls, lbl in curves:
            sub = df[df["tp_hours"] == tp].sort_values("core_product_pct")
            if not sub.empty:
                ax.plot(sub["core_product_pct"], sub["required_tbr"],
                        color=col, marker=m, ls=ls, lw=2.2, ms=6, label=lbl)

        ax.set_xlim(0.0, 5.2)
        ax.set_ylim(1.0, 1.30)
        ax.set_xlabel(r"Core Product $\eta_f f_b$ (%)", fontweight="bold", fontsize=11)
        ax.set_ylabel(r"Required TBR ($\mathrm{TBR}_R$)", fontweight="bold", fontsize=11)
        ax.set_title("Abdou 2021 Figure 4: Required TBR vs Core Product",
                     fontsize=12, fontweight="bold")
        ax.grid(True, ls=":", alpha=0.6)
        ax.legend(loc="upper right", fontsize=8.5)
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_5(self, context: PipelineContext, out_path: Path, dpi: int, show_inset: bool = False) -> None:
        df = load_benchmark_data(context, "Fig05_tbr_vs_availability", [
            "group2_fig05_tbr_vs_availability_real.csv",
            "Fig05_tbr_vs_availability.csv",
            "Fig05_required_tbr_summary.csv",
            "required_tbr_summary.csv",
        ])
        if "simulated_required_tbr" not in df.columns:
            if "Required_TBR" in df.columns:
                df["simulated_required_tbr"] = df["Required_TBR"]
            elif "required_tbr" in df.columns:
                df["simulated_required_tbr"] = df["required_tbr"]
        if "availability_factor_pct" not in df.columns and "AF" in df.columns:
            df["availability_factor_pct"] = (df["AF"] * 100.0).round(1)
        if "core_product_pct" not in df.columns and "f_b" in df.columns and "eta_f" in df.columns:
            df["core_product_pct"] = (df["f_b"] * df["eta_f"] * 100.0).round(2)

        fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=dpi)

        ax.axhspan(1.00, 1.05, color="#A5D6A7", alpha=0.45, label=r"High-Confidence Window ($\leq 1.05$)")
        ax.axhspan(1.05, 1.15, color="#C8E6C9", alpha=0.35, label=r"Possible Self-Sufficiency ($1.05 < \mathrm{TBR}_R \leq 1.15$)")
        ax.axhline(1.15, color="#2E7D32", ls="--", lw=1.2)
        ax.axhline(1.05, color="#1B5E20", ls=":", lw=1.2)

        curves = [
            (0.5, "#795548", "D", ":", r"$\eta_f f_b = 0.5\%$"),
            (1.0, "#1E88E5", "^", "-", r"$\eta_f f_b = 1.0\%$ (Reference)"),
            (2.0, "#D32F2F", "s", "--", r"$\eta_f f_b = 2.0\%$"),
            (3.0, "#0D47A1", "o", "-.", r"$\eta_f f_b = 3.0\%$"),
        ]
        for prod_pct, col, m, ls, lbl in curves:
            sub = df[np.isclose(df["core_product_pct"], prod_pct, atol=0.05)].sort_values("availability_factor_pct")
            if not sub.empty:
                ax.plot(sub["availability_factor_pct"], sub["simulated_required_tbr"],
                        color=col, marker=m, ls=ls, lw=2.2, ms=6, label=lbl)

        ax.set_xlim(0, 102)
        ax.set_ylim(1.0, 1.30)
        ax.set_xlabel("Availability Factor AF (%)", fontweight="bold", fontsize=11)
        ax.set_ylabel(r"Required TBR ($\mathrm{TBR}_R$)", fontweight="bold", fontsize=11)
        ax.set_title("Abdou 2021 Figure 5: Required TBR vs Reactor Availability Factor",
                     fontsize=12, fontweight="bold")
        ax.grid(True, ls=":", alpha=0.6)
        ax.legend(loc="upper right", fontsize=8.5)

        # Inset for Table 5 (Optional, disabled by default to keep Figure 5 clean and unblocked)
        if show_inset:
            t5_sub = df[np.isclose(df["core_product_pct"], 0.09, atol=0.02)].sort_values("availability_factor_pct")
            if not t5_sub.empty:
                inset_ax = ax.inset_axes([0.15, 0.52, 0.38, 0.40])
                inset_ax.plot(t5_sub["availability_factor_pct"], t5_sub["simulated_required_tbr"],
                              color="#1565C0", marker="s", lw=1.8, ms=5, label="TRICYS Sim")
                if "published_table5_tbr" in t5_sub.columns:
                    valid_pub = t5_sub.dropna(subset=["published_table5_tbr"])
                    inset_ax.scatter(valid_pub["availability_factor_pct"], valid_pub["published_table5_tbr"],
                                     color="#D50000", s=40, zorder=5, label="Table 5 Pub")
                else:
                    table5_pub_map = {10.0: 5.05, 30.0: 2.67, 50.0: 2.16, 70.0: 1.94, 90.0: 1.85, 100.0: 1.82}
                    af_pts = [float(af) for af in t5_sub["availability_factor_pct"] if float(af) in table5_pub_map]
                    pub_pts = [table5_pub_map[af] for af in af_pts]
                    if pub_pts:
                        inset_ax.scatter(af_pts, pub_pts, color="#D50000", s=40, zorder=5, label="Table 5 Pub")
                inset_ax.set_title(r"Table 5: ITER $\eta_f f_b=0.09\%$", fontsize=8, fontweight="bold")
                inset_ax.set_xlabel("AF (%)", fontsize=7.5)
                inset_ax.set_ylabel(r"$\mathrm{TBR}_R$", fontsize=7.5)
                inset_ax.tick_params(labelsize=7)
                inset_ax.grid(True, ls=":", alpha=0.5)
                inset_ax.legend(fontsize=6.5, loc="upper right")

        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_6(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        df = load_benchmark_data(context, "Fig06_tbr_vs_dir", [
            "Fig06_required_tbr_summary.csv",
            "Fig06_tbr_vs_dir.csv",
            "group2_fig06_dir_sweep_real.csv",
            "required_tbr_summary.csv",
        ])
        if "required_tbr" not in df.columns and "Required_TBR" in df.columns:
            df["required_tbr"] = df["Required_TBR"]
        if "dir_fraction_pct" not in df.columns:
            for k in ["f_DIR", "tep.DIR", "DIR", "f_dir", "dir"]:
                if k in df.columns:
                    df["dir_fraction_pct"] = (df[k] * 100.0).round(1)
                    break
        if "core_product_pct" not in df.columns and "f_b" in df.columns and "eta_f" in df.columns:
            df["core_product_pct"] = (df["f_b"] * df["eta_f"] * 100.0).round(2)

        fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=dpi)

        ax.axhspan(1.00, 1.05, color="#A5D6A7", alpha=0.45, label=r"High-Confidence Window ($\leq 1.05$)")
        ax.axhspan(1.05, 1.15, color="#C8E6C9", alpha=0.35, label=r"Possible Self-Sufficiency ($1.05 < \mathrm{TBR}_R \leq 1.15$)")
        ax.axhline(1.15, color="#2E7D32", ls="--", lw=1.2)
        ax.axhline(1.05, color="#1B5E20", ls=":", lw=1.2)

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
                ax.plot(sub_plot["dir_fraction_pct"], sub_plot["required_tbr"],
                        color=col, marker=m, ls=ls, lw=2.2, ms=6, label=lbl)

        ax.set_xlim(8, 92)
        ax.set_ylim(1.0, 1.25)
        ax.set_xlabel("DIR Fraction (%)", fontweight="bold", fontsize=11)
        ax.set_ylabel(r"Required TBR ($\mathrm{TBR}_R$)", fontweight="bold", fontsize=11)
        ax.set_title("Abdou 2021 Figure 6: Mitigation of Required TBR via DIR Bypass",
                     fontsize=12, fontweight="bold")
        ax.grid(True, ls=":", alpha=0.6)
        ax.legend(loc="upper right", fontsize=8.5)
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_7(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        self._plot_doubling_figure(context, out_path, dpi, [
            "group2_fig07_doubling_4h_real.csv",
            "Fig07_tbr_vs_doubling_time_4h.csv",
            "Fig07_required_tbr_summary.csv",
            "required_tbr_summary.csv"
        ], "30%", 1.30, "Figure 7: Required TBR vs Core Product for Doubling Times (Near-Term)")

    def _plot_figure_8(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        self._plot_doubling_figure(context, out_path, dpi, [
            "group2_fig08_doubling_1h_real.csv",
            "Fig08_tbr_vs_doubling_time_1h.csv",
            "Fig08_required_tbr_summary.csv",
            "required_tbr_summary.csv"
        ], "80%", 1.25, "Figure 8: Required TBR vs Core Product for Doubling Times (Commercial)")

    def _plot_doubling_figure(self, context: PipelineContext, out_path: Path, dpi: int, csv_name, af_str: str, y_max: float, title: str) -> None:
        cands = [csv_name] if isinstance(csv_name, str) else list(csv_name)
        df = load_benchmark_data(context, title, cands)
        td_col_map = {
            1.0: ["Required_TBR(8766.0 units)", "Required_TBR_1yr", "Required_TBR(8766.0)"],
            3.0: ["Required_TBR(26298.0 units)", "Required_TBR_3yr", "Required_TBR(26298.0)"],
            5.0: ["Required_TBR(43830.0 units)", "Required_TBR_5yr", "Required_TBR(43830.0)"],
            7.0: ["Required_TBR(61362.0 units)", "Required_TBR_7yr", "Required_TBR(61362.0)"],
        }
        if "td_years" not in df.columns:
            rows = []
            has_wide = any(any(c in df.columns for c in cands) for cands in td_col_map.values())
            if has_wide:
                for _, r in df.iterrows():
                    cp = (r["f_b"] * r["eta_f"] * 100.0) if ("f_b" in r and "eta_f" in r) else r.get("core_product_pct", 0.0)
                    for td_yr, cands in td_col_map.items():
                        for c in cands:
                            if c in r and pd.notna(r[c]):
                                rows.append({
                                    "td_years": td_yr,
                                    "core_product_pct": cp,
                                    "required_tbr": float(r[c]),
                                })
                                break
                if rows:
                    df = pd.DataFrame(rows)
            elif "t_d" in df.columns:
                df["td_years"] = (df["t_d"] / (365.25 * 24.0)).round(1)

        if "required_tbr" not in df.columns and "Required_TBR" in df.columns:
            df["required_tbr"] = df["Required_TBR"]
        if "core_product_pct" not in df.columns and "f_b" in df.columns and "eta_f" in df.columns:
            df["core_product_pct"] = (df["f_b"] * df["eta_f"] * 100.0).round(2)

        fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=dpi)

        ax.axhspan(1.00, 1.05, color="#A5D6A7", alpha=0.45, label=r"High-Confidence Window ($\leq 1.05$)")
        ax.axhspan(1.05, 1.15, color="#C8E6C9", alpha=0.35, label=r"Possible Self-Sufficiency ($1.05 < \mathrm{TBR}_R \leq 1.15$)")
        ax.axhline(1.15, color="#2E7D32", ls="--", lw=1.2)
        ax.axhline(1.05, color="#1B5E20", ls=":", lw=1.2)

        curves = [
            (1.0, "#0288D1", "o", ":", r"$t_d = 1$ yr"),
            (3.0, "#D32F2F", "s", "--", r"$t_d = 3$ yr"),
            (5.0, "#7B1FA2", "^", "-.", r"$t_d = 5$ yr (Reference)"),
            (7.0, "#0D47A1", "*", "-", r"$t_d = 7$ yr"),
        ]
        for td, col, m, ls, lbl in curves:
            sub = df[df["td_years"] == td].sort_values("core_product_pct")
            sub_plot = sub[sub["required_tbr"] <= y_max + 0.15]
            ax.plot(sub_plot["core_product_pct"], sub_plot["required_tbr"],
                    color=col, marker=m, ls=ls, lw=2.2, ms=6, label=lbl)

        ax.set_xlim(0.0, 5.2)
        ax.set_ylim(1.0, y_max)
        ax.set_xlabel(r"Core Product $\eta_f f_b$ (%)", fontweight="bold", fontsize=11)
        ax.set_ylabel(r"Required TBR ($\mathrm{TBR}_R$)", fontweight="bold", fontsize=11)
        ax.set_title(f"Abdou 2021 {title}", fontsize=11.5, fontweight="bold")
        ax.grid(True, ls=":", alpha=0.6)
        ax.legend(loc="upper right", fontsize=8.5)
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_14(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        df = load_benchmark_data(context, "Fig14_tbr_vs_reserve_time", [
            "Fig14_required_tbr_summary.csv",
            "Fig14_tbr_vs_reserve_time.csv",
            "group3_fig12_14_reserve_time.csv",
            "required_tbr_summary.csv"
        ])
        if "required_tbr" not in df.columns and "Required_TBR" in df.columns:
            df["required_tbr"] = df["Required_TBR"]
        if "core_product_pct" not in df.columns and "f_b" in df.columns and "eta_f" in df.columns:
            df["core_product_pct"] = (df["f_b"] * df["eta_f"] * 100.0).round(2)
        tr_col = "t_r" if "t_r" in df.columns else "reserve_time_tr_hours"

        fig, ax = plt.subplots(figsize=(8.5, 6), dpi=dpi)

        curves = [
            (0.5, "#D32F2F", "o", "-", r"$\eta_f f_b = 0.5\%$"),
            (1.0, "#EF6C00", "s", "--", r"$\eta_f f_b = 1.0\%$"),
            (2.0, "#2E7D32", "^", "-.", r"$\eta_f f_b = 2.0\%$"),
            (5.0, "#1565C0", "d", ":", r"$\eta_f f_b = 5.0\%$"),
        ]
        for prod_pct, col, m, ls, lbl in curves:
            sub = df[np.isclose(df["core_product_pct"], prod_pct, atol=0.05)].sort_values(tr_col)
            if not sub.empty:
                ax.plot(sub[tr_col], sub["required_tbr"],
                        color=col, marker=m, ls=ls, lw=2.2, label=lbl)

        ax.axhline(1.15, color="#7B1FA2", linestyle="--", lw=1.5, label="Achievable Limit (1.15)")
        ax.set_xlim(0, 48)
        ax.set_ylim(0.98, 1.45)
        ax.set_xlabel("Reserve Time $t_r$ (hours)", fontsize=11, fontweight="bold")
        ax.set_ylabel(r"Required Tritium Breeding Ratio ($\mathrm{TBR}_R$)", fontsize=11, fontweight="bold")
        ax.set_title("Abdou 2021 Figure 14: Effect of Reserve Time on Required TBR", fontsize=12, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(frameon=True, loc="upper left")
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_17(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        df = load_benchmark_data(context, "Fig17_fnsf_tbr_scenarios", ["group2_fig17_fnsf_scenarios.csv"])
        fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=dpi)

        p = df["fusion_power_MW"]
        ax.plot(p, df["tbr_scenario_1_zero_supply"], color="#D32F2F", lw=2.5, marker="o", label="Scenario 1: Zero External Supply")
        ax.plot(p, df["tbr_scenario_2_5kg_supply"], color="#F57C00", lw=2.2, ls="--", marker="s", label="Scenario 2: 5 kg External Supply Available")
        ax.plot(p, df["tbr_scenario_3_10kg_supply"], color="#2E7D32", lw=2.2, ls="-.", marker="^", label="Scenario 3: 10 kg External Supply Available")

        ax.axhline(1.0, color="#616161", linestyle=":", lw=1.2, label="Breakeven TBR = 1.0")
        ax.axhline(1.15, color="#7B1FA2", linestyle="--", lw=1.2, label="Max Achievable Limit (1.15)")

        ax.set_xlim(50, 300)
        ax.set_ylim(0.4, 1.6)
        ax.set_xlabel("FNSF Fusion Power (MW)", fontsize=11, fontweight="bold")
        ax.set_ylabel(r"Required Tritium Breeding Ratio ($\mathrm{TBR}_R$)", fontsize=11, fontweight="bold")
        ax.set_title("Abdou 2021 Figure 17: FNSF Required TBR Under External Supply Scenarios", fontsize=12, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(frameon=True, loc="upper right")
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _export_group2_data(self, csv_path: Path, context: PipelineContext) -> None:
        try:
            df = load_benchmark_data(context, "group2_export", ["group2_fig05_tbr_vs_availability_real.csv"])
            t5_sub = df[np.isclose(df["core_product_pct"], 0.09, atol=0.02)].sort_values("availability_factor_pct")
            records = []
            for _, row in t5_sub.iterrows():
                af = row["availability_factor"]
                pub = row["published_table5_tbr"]
                sim = row["simulated_required_tbr"]
                err = abs(sim - pub) / pub * 100.0 if pd.notna(pub) else 0.0
                records.append({
                    "availability_factor": af,
                    "af_pct": af * 100.0,
                    "published_table5_tbr": pub,
                    "tricys_vv_calculated_tbr": round(sim, 2),
                    "relative_error_pct": round(err, 2),
                })
            df_g2 = pd.DataFrame(records)
            df_g2.to_csv(csv_path, index=False)
            context.artifacts["group2_self_sufficiency_data"] = str(csv_path)
        except Exception as e:
            logger.warning(f"Could not export group2 data: {e}")
