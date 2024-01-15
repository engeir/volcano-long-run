"""Initializes the package volcano-long-run."""

from importlib.metadata import version

from vlr import config, download, utils

__all__ = ["config", "utils", "download"]

__version__ = version("volcano-long-run")
