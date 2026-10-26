"""Individual dedicated single-figure plugins (18 plugins) for Abdou 2021 V&V.
"""

from __future__ import annotations

import logging
from pathlib import Path

from tricys.workflow.base import PluginMetadata, PostprocessPlugin
from tricys.workflow.context import PipelineContext
from tricys.workflow.registry import register_postprocess_plugin
from .group1 import AbdouGroup1Plugin
from .group2 import AbdouGroup2Plugin
from .group3 import AbdouGroup3Plugin
from .master import AbdouBenchmarkMasterPlugin

logger = logging.getLogger(__name__)


class _SingleFigurePluginBase(PostprocessPlugin):
    """Base class for dedicated per-figure plugins matching Abdou 2021."""

    figure_key: str = ""
    target_class: type = None
    target_method: str = ""

    @classmethod
    def get_metadata(cls) -> PluginMetadata:
        return PluginMetadata(
            name=cls.name,
            category="postprocess",
            description=f"Dedicated single-figure plugin for Abdou 2021 {cls.figure_key}.",
            version="2.0.0",
            author="TRICYS V&V Team",
            parameters_schema={"dpi": {"type": "integer", "default": 300}},
            output_artifacts=[f"{cls.figure_key}.png"],
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
        out_path = fig_dir / f"{self.figure_key}.png"

        # Instantiate target handler and run directly with context
        handler = self.target_class(dpi=dpi, output_dir=str(out_dir))
        fn = getattr(handler, self.target_method)

        if self.target_method == "_plot_figure_1":
            fn(out_path, dpi)
        elif self.target_method == "_plot_figure_3_and_export":
            csv_path = data_dir / "group1_dynamics_data.csv"
            fn(context, out_path, csv_path, dpi)
        elif self.target_method == "_plot_figure_5":
            show_inset = bool(self.params.get("show_inset", False))
            fn(context, out_path, dpi, show_inset=show_inset)
        else:
            fn(context, out_path, dpi)

        context.artifacts[self.figure_key] = str(out_path)
        logger.info(f"[{self.name}] Successfully generated: {out_path.name}")


@register_postprocess_plugin("abdou_fig01_topology")
class AbdouFig01Plugin(_SingleFigurePluginBase):
    name = "abdou_fig01_topology"
    figure_key = "Fig01_fuel_cycle_topology"
    target_class = AbdouGroup1Plugin
    target_method = "_plot_figure_1"


@register_postprocess_plugin("abdou_fig02_starvation_valley")
class AbdouFig02Plugin(_SingleFigurePluginBase):
    name = "abdou_fig02_starvation_valley"
    figure_key = "Fig02_starvation_valley_dynamics"
    target_class = AbdouGroup1Plugin
    target_method = "_plot_figure_2"


@register_postprocess_plugin("abdou_fig03_inventory_evolution")
class AbdouFig03Plugin(_SingleFigurePluginBase):
    name = "abdou_fig03_inventory_evolution"
    figure_key = "Fig03_inventory_evolution"
    target_class = AbdouGroup1Plugin
    target_method = "_plot_figure_3_and_export"


@register_postprocess_plugin("abdou_fig04_tbr_vs_burnup")
class AbdouFig04Plugin(_SingleFigurePluginBase):
    name = "abdou_fig04_tbr_vs_burnup"
    figure_key = "Fig04_tbr_vs_burnup"
    target_class = AbdouGroup2Plugin
    target_method = "_plot_figure_4"


@register_postprocess_plugin("abdou_fig05_tbr_vs_availability")
class AbdouFig05Plugin(_SingleFigurePluginBase):
    name = "abdou_fig05_tbr_vs_availability"
    figure_key = "Fig05_tbr_vs_availability"
    target_class = AbdouGroup2Plugin
    target_method = "_plot_figure_5"


@register_postprocess_plugin("abdou_fig06_tbr_vs_dir")
class AbdouFig06Plugin(_SingleFigurePluginBase):
    name = "abdou_fig06_tbr_vs_dir"
    figure_key = "Fig06_tbr_vs_dir"
    target_class = AbdouGroup2Plugin
    target_method = "_plot_figure_6"


@register_postprocess_plugin("abdou_fig07_tbr_vs_doubling_time_4h")
class AbdouFig07Plugin(_SingleFigurePluginBase):
    name = "abdou_fig07_tbr_vs_doubling_time_4h"
    figure_key = "Fig07_tbr_vs_doubling_time_4h"
    target_class = AbdouGroup2Plugin
    target_method = "_plot_figure_7"


@register_postprocess_plugin("abdou_fig08_tbr_vs_doubling_time_1h")
class AbdouFig08Plugin(_SingleFigurePluginBase):
    name = "abdou_fig08_tbr_vs_doubling_time_1h"
    figure_key = "Fig08_tbr_vs_doubling_time_1h"
    target_class = AbdouGroup2Plugin
    target_method = "_plot_figure_8"


@register_postprocess_plugin("abdou_fig09_global_tritium_supply")
class AbdouFig09Plugin(_SingleFigurePluginBase):
    name = "abdou_fig09_global_tritium_supply"
    figure_key = "Fig09_global_tritium_supply_2000_2060"
    target_class = AbdouGroup3Plugin
    target_method = "_plot_figure_9"


@register_postprocess_plugin("abdou_fig10_startup_inventory_vs_burnup")
class AbdouFig10Plugin(_SingleFigurePluginBase):
    name = "abdou_fig10_startup_inventory_vs_burnup"
    figure_key = "Fig10_startup_inventory_vs_burnup"
    target_class = AbdouGroup3Plugin
    target_method = "_plot_figure_10"


@register_postprocess_plugin("abdou_fig11_startup_inventory_vs_dir")
class AbdouFig11Plugin(_SingleFigurePluginBase):
    name = "abdou_fig11_startup_inventory_vs_dir"
    figure_key = "Fig11_startup_inventory_vs_dir"
    target_class = AbdouGroup3Plugin
    target_method = "_plot_figure_11"


@register_postprocess_plugin("abdou_fig12_startup_inventory_vs_reserve_time")
class AbdouFig12Plugin(_SingleFigurePluginBase):
    name = "abdou_fig12_startup_inventory_vs_reserve_time"
    figure_key = "Fig12_startup_inventory_vs_reserve_time"
    target_class = AbdouGroup3Plugin
    target_method = "_plot_figure_12"


@register_postprocess_plugin("abdou_fig13_reserve_inventory_vs_reserve_time")
class AbdouFig13Plugin(_SingleFigurePluginBase):
    name = "abdou_fig13_reserve_inventory_vs_reserve_time"
    figure_key = "Fig13_reserve_inventory_vs_reserve_time"
    target_class = AbdouGroup3Plugin
    target_method = "_plot_figure_13"


@register_postprocess_plugin("abdou_fig14_tbr_vs_reserve_time")
class AbdouFig14Plugin(_SingleFigurePluginBase):
    name = "abdou_fig14_tbr_vs_reserve_time"
    figure_key = "Fig14_tbr_vs_reserve_time"
    target_class = AbdouGroup2Plugin
    target_method = "_plot_figure_14"


@register_postprocess_plugin("abdou_fig15_startup_inventory_vs_power")
class AbdouFig15Plugin(_SingleFigurePluginBase):
    name = "abdou_fig15_startup_inventory_vs_power"
    figure_key = "Fig15_startup_inventory_vs_power"
    target_class = AbdouGroup3Plugin
    target_method = "_plot_figure_15"


@register_postprocess_plugin("abdou_fig16_reactor_comparison_startup")
class AbdouFig16Plugin(_SingleFigurePluginBase):
    name = "abdou_fig16_reactor_comparison_startup"
    figure_key = "Fig16_reactor_comparison_startup"
    target_class = AbdouGroup3Plugin
    target_method = "_plot_figure_16"


@register_postprocess_plugin("abdou_fig17_fnsf_tbr_scenarios")
class AbdouFig17Plugin(_SingleFigurePluginBase):
    name = "abdou_fig17_fnsf_tbr_scenarios"
    figure_key = "Fig17_fnsf_tbr_scenarios"
    target_class = AbdouGroup2Plugin
    target_method = "_plot_figure_17"


@register_postprocess_plugin("abdou_synthesis_poster")
class AbdouSynthesisPlugin(_SingleFigurePluginBase):
    name = "abdou_synthesis_poster"
    figure_key = "Fig_Abdou2021_Synthesis"
    target_class = AbdouBenchmarkMasterPlugin
    target_method = "_plot_synthesis_poster"
