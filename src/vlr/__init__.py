"""Initializes the package volcano-long-run."""

from importlib.metadata import version

import matplotlib as mpl
import nc_time_axis

from vlr import config, create, download
from vlr.utils import find_c2w_files, load_historic_data, time_series

__all__ = [
    "config",
    "create",
    "download",
    "find_c2w_files",
    "load_historic_data",
    "nc_time_axis",
    "time_series",
]

__version__ = version("volcano-long-run")

mpl.style.use(
    "https://raw.githubusercontent.com/uit-cosmo/cosmoplots/main/cosmoplots/default.mplstyle"
)
