"""Group 1: Fuel cycle topology, storage starvation dynamics & 15-subsystem inventory.
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

from tricys.workflow.base import PluginMetadata, PostprocessPlugin
from tricys.workflow.context import PipelineContext
from tricys.workflow.registry import register_postprocess_plugin
from .common import load_benchmark_data

logger = logging.getLogger(__name__)


@register_postprocess_plugin("abdou_group1_dynamics")
class AbdouGroup1Plugin(PostprocessPlugin):
    """Postprocessing plugin for Abdou 2021 Group 1 benchmarks (Figures 1, 2, 3)."""

    name = "abdou_group1_dynamics"

    @classmethod
    def get_metadata(cls) -> PluginMetadata:
        return PluginMetadata(
            name=cls.name,
            category="postprocess",
            description="Abdou 2021 Group 1: Fuel cycle topology, starvation valley dynamics & 15-subsystem inventory.",
            version="2.0.0",
            author="TRICYS V&V Team",
            parameters_schema={
                "dpi": {"type": "integer", "default": 300},
                "output_dir": {"type": "string", "default": ""},
            },
            input_requirements=["results_dir"],
            output_artifacts=[
                "Fig01_fuel_cycle_topology.png",
                "Fig02_starvation_valley_dynamics.png",
                "Fig03_inventory_evolution.png",
                "group1_dynamics_data.csv",
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

        logger.info(f"[{self.name}] Generating Group 1 publication figures...")

        # 1. Figure 1: Flowsheet Topology
        self._plot_figure_1(fig_dir / "Fig01_fuel_cycle_topology.png", dpi)

        # 2. Figure 2: Starvation Valley Dynamics
        self._plot_figure_2(context, fig_dir / "Fig02_starvation_valley_dynamics.png", dpi)

        # 3. Figure 3: 15-Subsystem Inventory Evolution & CSV Export
        self._plot_figure_3_and_export(context, fig_dir / "Fig03_inventory_evolution.png", data_dir / "group1_dynamics_data.csv", dpi)

        logger.info(f"[{self.name}] Group 1 completed successfully.")

    def _plot_figure_1(self, out_path: Path, dpi: int) -> None:
        fig, ax = plt.subplots(figsize=(13, 8), dpi=dpi)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 70)
        ax.axis("off")

        # Color palette
        c_plasma = "#E64B35"
        c_inner = "#4DBBD5"
        c_outer = "#00A087"
        c_storage = "#3C5488"
        c_loss = "#7E6148"

        def draw_box(x, y, w, h, text, color, subtext=""):
            rect = patches.FancyBboxPatch(
                (x, y), w, h, boxstyle="round,pad=0.8",
                facecolor=color, edgecolor="#2C3E50", linewidth=1.5, alpha=0.9
            )
            ax.add_patch(rect)
            ax.text(x + w / 2, y + h / 2 + (1.2 if subtext else 0), text,
                    ha="center", va="center", color="white", fontsize=11, fontweight="bold")
            if subtext:
                ax.text(x + w / 2, y + h / 2 - 1.8, subtext,
                        ha="center", va="center", color="#F8F9FA", fontsize=8.5, style="italic")

        def draw_arrow(x1, y1, x2, y2, label="", color="#2C3E50", rad=0.0):
            ax.annotate(
                "", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0,
                                connectionstyle=f"arc3,rad={rad}", mutation_scale=15)
            )
            if label:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                ax.text(mx, my + 1.2, label, ha="center", va="bottom",
                        fontsize=8.5, fontweight="semibold", color=color,
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.8))

        # Inner Fuel Cycle (IFC) Nodes
        draw_box(42, 54, 16, 9, "Plasma Core", c_plasma, "Burn: fb=0.36%-5%")
        draw_box(42, 38, 16, 8, "Vacuum Pumping", c_inner, "Cryopumps / Mercury")
        draw_box(42, 24, 16, 8, "Fuel Cleanup (FCU)", c_inner, "DIR Bypass Option")
        draw_box(42, 10, 16, 8, "Isotope Separation", c_inner, "ISS Cryogenic Columns")
        draw_box(14, 10, 16, 8, "Storage System", c_storage, "SDS Hydride Beds")
        draw_box(14, 38, 16, 8, "Fueling System", c_inner, "HFS Pellet Injector")

        # Outer Fuel Cycle (OFC) Nodes
        draw_box(74, 54, 18, 9, "Blanket (BZ)", c_outer, "Ceramic / PbLi Breeds T")
        draw_box(74, 38, 18, 8, "Tritium Extraction", c_outer, "TES (Purge / Permeator)")
        draw_box(74, 24, 18, 8, "Coolant Purif. (CPS)", c_outer, "PFC / BZ Coolant Loops")
        draw_box(74, 10, 18, 8, "Water Detritiation", c_loss, "WDS / Exhaust Detrit.")

        # Flow Connections
        draw_arrow(50, 54, 50, 46, "Exhaust (1-fb)")
        draw_arrow(50, 38, 50, 32, "Rough Gas")
        draw_arrow(50, 24, 50, 18, "H2/D2/T2 mix")
        draw_arrow(42, 14, 30, 14, "Pure T2 / DT")
        draw_arrow(22, 18, 22, 38, "Feed from Storage")
        draw_arrow(22, 46, 42, 58, "Pellet Injection (eta_f)", rad=0.2)

        # DIR Bypass (Orange)
        draw_arrow(42, 28, 26, 38, "DIR Bypass (80%-90%)", color="#D9534F", rad=-0.25)

        # OFC Connections
        draw_arrow(58, 58, 74, 58, "14 MeV Neutrons (TBR)", color="#00A087")
        draw_arrow(83, 54, 83, 46, "He Purge Gas")
        draw_arrow(83, 38, 58, 14, "Recovered T", rad=0.2)
        draw_arrow(83, 24, 83, 18, "Permeation")

        ax.set_title("Abdou 2021 Figure 1: Fusion Reactor Inner & Outer Fuel Cycle Architecture",
                     fontsize=14, fontweight="bold", pad=15)
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_2(self, context: PipelineContext, out_path: Path, dpi: int) -> None:
        """Figure 2: Starvation Valley Dynamics from real simulation data."""
        df = load_benchmark_data(context, "Fig02_starvation_valley_dynamics", ["group1_dynamics_data.csv", "simulation_results.csv"])
        fig, ax = plt.subplots(figsize=(9, 6), dpi=dpi)

        t_d = df["time_d"]
        I_s = df["sds.inventory"]
        min_idx = I_s.idxmin()
        t_min = t_d.loc[min_idx]
        I_min = I_s.loc[min_idx]

        ax.plot(t_d, I_s, color="#1B5E20", lw=2.5, label=r"Storage Inventory $I_S(t)$ (Dynamic Simulation)")
        ax.axvspan(6.0, 8.0, color="#FFF9C4", alpha=0.5, label="Abdou Starvation Nadir Window (Day 6–8)")
        ax.axvline(t_min, color="#D32F2F", ls="--", lw=1.2)
        ax.scatter([t_min], [I_min], color="#D32F2F", s=60, zorder=5)

        ax.set_xlabel("Operational Time (Days)", fontsize=11, fontweight="bold")
        ax.set_ylabel(r"Storage Tritium Inventory $I_S(t)$ (g)", fontsize=11, fontweight="bold")
        ax.set_title("Abdou 2021 Figure 2: Storage Tritium Inventory Dynamics & Startup Starvation Valley",
                     fontsize=12, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(frameon=True, loc="upper right")
        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)

    def _plot_figure_3_and_export(self, context: PipelineContext, out_path: Path, csv_path: Path, dpi: int) -> None:
        """Figure 3: 15-Subsystem dynamic inventory evolution strictly from real simulation data."""
        df = load_benchmark_data(context, "Fig03_inventory_evolution", ["group1_dynamics_data.csv", "simulation_results.csv"])

        # Export group 1 data artifact
        df.to_csv(csv_path, index=False)
        context.artifacts["group1_dynamics_data"] = str(csv_path)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.5, 8.0), dpi=dpi, sharex=True)
        t_d = df["time_d"]

        # Panel 1: Key subsystems in kg
        if "sds.inventory" in df.columns:
            ax1.plot(t_d, df["sds.inventory"] / 1000.0, color="#1B5E20", lw=2.5, ls="-", label="Storage SDS ($I_S(t)$)")
        if "i_iss.inventory" in df.columns:
            ax1.plot(t_d, df["i_iss.inventory"] / 1000.0, color="#7B1FA2", lw=2.0, ls="--", label="Isotope Separation I-ISS")
        if "bz.inventory" in df.columns:
            ax1.plot(t_d, df["bz.inventory"] / 1000.0, color="#F57F17", lw=2.0, ls=":", label="Breeding Zone BZ")
        if "tes.inventory" in df.columns:
            ax1.plot(t_d, df["tes.inventory"] / 1000.0, color="#00838F", lw=2.0, ls="-.", label="Extraction TES")
        if "tep.inventory" in df.columns:
            ax1.plot(t_d, df["tep.inventory"] / 1000.0, color="#EF6C00", lw=1.8, ls=(0, (3, 1, 1, 1)), label="Fuel Cleanup TEP")
        if "plant_total_inv" in df.columns:
            ax1.plot(t_d, df["plant_total_inv"] / 1000.0, color="#424242", lw=2.0, ls="-", alpha=0.7, label="Plant Total Inventory")

        ax1.axvspan(6.0, 8.0, color="#FFF9C4", alpha=0.5, label="Abdou Starvation Nadir Window (Day 6–8)")
        ax1.set_ylabel("Tritium Inventory (kg)", fontweight="bold")
        ax1.set_title("Abdou 2021 Figure 3: Dynamic Tritium Inventory Evolution Across 15 Subsystems (500h)",
                      fontsize=11.5, fontweight="bold")
        ax1.grid(True, ls=":", alpha=0.6)
        ax1.legend(loc="upper right", fontsize=8.5, ncol=2)

        # Panel 2: Balance-of-Plant, Coolant & Recovery Subsystems in grams
        sub_configs = [
            ("ps.inventory", "Pumping & Injection PS", "#D81B60", "-"),
            ("cps_pfc.inventory", "CPS-PFC", "#3949AB", "-"),
            ("o_iss.inventory", "Outer ISS (O-ISS)", "#8E24AA", "-"),
            ("coolant_FW.inventory", "Coolant FW", "#00897B", "--"),
            ("coolant_DIV.inventory", "Coolant DIV", "#43A047", "--"),
            ("cps_bz.inventory", "CPS-BZ", "#FB8C00", ":"),
            ("wds.inventory", "Water Detritiation WDS", "#039BE5", ":"),
            ("coolant_S_CO2.inventory", "Coolant S-CO2", "#6D4C41", "-."),
            ("fw.inventory", "First Wall (FW)", "#546E7A", "-"),
            ("div.inventory", "Divertor (DIV)", "#78909C", "-"),
            ("vds.inventory", "Vent Detritiation VDS", "#26A69A", ":"),
        ]
        for col, label, color, ls in sub_configs:
            if col in df.columns:
                ax2.plot(t_d, df[col], color=color, lw=1.4, ls=ls, label=label)

        ax2.set_xlabel("Time (Days)", fontweight="bold")
        ax2.set_ylabel("Subsystem Inventory (g)", fontweight="bold")
        ax2.grid(True, ls=":", alpha=0.6)
        ax2.legend(loc="upper right", fontsize=7.5, ncol=3)

        plt.tight_layout()
        plt.savefig(out_path, dpi=dpi)
        plt.close(fig)
        context.artifacts["Fig03_inventory_evolution"] = str(out_path)
