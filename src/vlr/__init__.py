"""Initializes the package volcano-long-run."""

from importlib.metadata import version

import nc_time_axis
from matplotlib import style as mpl_style

from vlr import create

__all__ = [
    "create",
    "nc_time_axis",
]

__version__ = version("volcano-long-run")

mpl_style.use(
    "https://raw.githubusercontent.com/uit-cosmo/cosmoplots/main/cosmoplots/default.mplstyle"
)
