import os
from pathlib import Path

from matplotlib.figure import Figure

from ash_model_plotting.plotting import (
    draw_2d_cube, plot_3d_cube, plot_4d_cube
)


def test_plot_4d_happy_path(name_model_result, tmpdir, scantree):
    cube = name_model_result.air_concentration
    expected = [
        '01000/VA_Tutorial_Air_Concentration_01000_20100418030000.png',
        '01000/VA_Tutorial_Air_Concentration_01000_20100418060000.png',
        '00500/VA_Tutorial_Air_Concentration_00500_20100418030000.png',
        '00500/VA_Tutorial_Air_Concentration_00500_20100418060000.png',
        ]

    plot_4d_cube(cube, tmpdir)

    plot_files = [Path(entry).relative_to(tmpdir).as_posix()
                  for entry in scantree(tmpdir) if entry.is_file()]

    assert plot_files == expected


def test_plot_4d_vmax_and_bbox_inches(name_model_result, tmpdir, scantree):
    """
    Check that **kwargs are passed to called functions. Only check that they
    haven't caused a crash - visual check determines if they worked
    """
    cube = name_model_result.air_concentration
    expected = [
        '01000/VA_Tutorial_Air_Concentration_01000_20100418030000.png',
        '01000/VA_Tutorial_Air_Concentration_01000_20100418060000.png',
        '00500/VA_Tutorial_Air_Concentration_00500_20100418030000.png',
        '00500/VA_Tutorial_Air_Concentration_00500_20100418060000.png',
    ]

    plot_4d_cube(cube, tmpdir, vmax=cube.data.max(), bbox_inches='tight')

    plot_files = [Path(entry).relative_to(tmpdir).as_posix()
                  for entry in scantree(tmpdir) if entry.is_file()]

    assert plot_files == expected


def test_plot_3d_vmax_and_bbox_inches(name_model_result, tmpdir):
    """
    Check that **kwargs are passed to called functions. Only check that they
    haven't caused a crash - visual check determines if they worked
    """
    cube = name_model_result.total_deposition
    expected = ['VA_Tutorial_Total_deposition_20100418030000.png',
                'VA_Tutorial_Total_deposition_20100418060000.png']

    plot_3d_cube(cube, tmpdir, vmax=cube.data.max(), bbox_inches='tight')
    plot_files = os.listdir(tmpdir)

    assert plot_files == expected


def test_plot_3d_happy_path(name_model_result, tmpdir):
    cube = name_model_result.total_deposition
    expected = ['VA_Tutorial_Total_deposition_20100418030000.png',
                'VA_Tutorial_Total_deposition_20100418060000.png']

    plot_3d_cube(cube, tmpdir)
    plot_files = os.listdir(tmpdir)

    assert plot_files == expected


def test_plot_2d_happy_path(name_model_result):
    cube = name_model_result.air_concentration[0, 0, :, :]
    fig, title = draw_2d_cube(cube)

    assert isinstance(fig, Figure)
    assert title == 'VA_Tutorial_Air_Concentration_00500_20100418030000'


def test_plot_2d_no_altitude(name_model_result):
    cube = name_model_result.total_deposition[0, :, :]
    fig, title = draw_2d_cube(cube)

    assert isinstance(fig, Figure)
    assert title == 'VA_Tutorial_Total_deposition_20100418030000'
