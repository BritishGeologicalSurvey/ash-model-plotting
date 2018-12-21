from matplotlib.figure import Figure
import pytest

from ash_model_plotting.plotting import plot_2d_cube


def test_plot_2d_happy_path(name_model_result):
    cube = name_model_result.air_concentration[0, 0, :, :]
    fig, title = plot_2d_cube(cube)

    assert isinstance(fig, Figure)
    assert title == 'VA_Tutorial_Air_Concentration_00500_20100418030000'


def test_plot_2d_no_altitude(name_model_result):
    cube = name_model_result.total_deposition[0, :, :]
    fig, title = plot_2d_cube(cube)

    assert isinstance(fig, Figure)
    assert title == 'VA_Tutorial_Total_deposition_20100418030000'
