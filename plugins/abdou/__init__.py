"""Abdou 2021 Tritium Fuel Cycle Benchmark & Verification Plugins.

This package provides postprocessing plugins for:
- Group 1: Fuel cycle topology, storage starvation dynamics & 15-subsystem inventory.
- Group 2: Tritium self-sufficiency phase space, required TBR sweeps.
- Group 3: Startup inventory collapse, reserve time scaling & global tritium supply.
- Master: Comprehensive synthesis and overview poster.
- 18 Individual per-figure plugins.
"""

from __future__ import annotations

from .common import (
    YEARS_TO_HOURS,
    TRITIUM_HALF_LIFE_YEARS,
    LAMBDA_PER_HOUR,
    get_burn_rate_g_per_h,
    load_benchmark_data,
)
from .group1 import AbdouGroup1Plugin
from .group2 import AbdouGroup2Plugin
from .group3 import AbdouGroup3Plugin
from .master import AbdouBenchmarkMasterPlugin
from .figures import (
    _SingleFigurePluginBase,
    AbdouFig01Plugin,
    AbdouFig02Plugin,
    AbdouFig03Plugin,
    AbdouFig04Plugin,
    AbdouFig05Plugin,
    AbdouFig06Plugin,
    AbdouFig07Plugin,
    AbdouFig08Plugin,
    AbdouFig09Plugin,
    AbdouFig10Plugin,
    AbdouFig11Plugin,
    AbdouFig12Plugin,
    AbdouFig13Plugin,
    AbdouFig14Plugin,
    AbdouFig15Plugin,
    AbdouFig16Plugin,
    AbdouFig17Plugin,
    AbdouSynthesisPlugin,
)

__all__ = [
    "YEARS_TO_HOURS",
    "TRITIUM_HALF_LIFE_YEARS",
    "LAMBDA_PER_HOUR",
    "get_burn_rate_g_per_h",
    "load_benchmark_data",
    "AbdouGroup1Plugin",
    "AbdouGroup2Plugin",
    "AbdouGroup3Plugin",
    "AbdouBenchmarkMasterPlugin",
    "_SingleFigurePluginBase",
    "AbdouFig01Plugin",
    "AbdouFig02Plugin",
    "AbdouFig03Plugin",
    "AbdouFig04Plugin",
    "AbdouFig05Plugin",
    "AbdouFig06Plugin",
    "AbdouFig07Plugin",
    "AbdouFig08Plugin",
    "AbdouFig09Plugin",
    "AbdouFig10Plugin",
    "AbdouFig11Plugin",
    "AbdouFig12Plugin",
    "AbdouFig13Plugin",
    "AbdouFig14Plugin",
    "AbdouFig15Plugin",
    "AbdouFig16Plugin",
    "AbdouFig17Plugin",
    "AbdouSynthesisPlugin",
]
