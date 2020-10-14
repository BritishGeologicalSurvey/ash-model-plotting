"""Simplified plotting of dispersion model results."""
# flake8: noqa
# pylint: disable=wrong-import-position

# Tell matplotlib to use the 'Agg' backend for plotting
# We have to do this here, before importing Iris, as Iris
# will set it to TkAgg by default.
import matplotlib
matplotlib.use('Agg')

from ash_model_plotting.ash_model_results import (
    AshModelResult,
    NameAshModelResult,
    Fall3DAshModelResult,
    HysplitAshModelResult,
    AshModelResultError)

name = "ash_model_plotting"
