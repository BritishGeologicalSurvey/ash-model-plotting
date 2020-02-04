"""Unit tests for plotting module."""
import os
from pathlib import Path

from matplotlib.figure import Figure  # noqa

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
    expected_metadata = {
        'created_by': 'plot_4d_cube',
        'attributes': {'End of release': '0800UTC 17/04/2010',
                       'Forecast duration': '75 hours',
                       'Met data': 'NWP Flow.ECMWF ERAInt Regional',
                       'NAME Version': 'NAME III (version 7.2)',
                       'Release height': '1651.000 to 6151.000m asl',
                       'Release location': '19.3600W   63.3700N',
                       'Release rate': '9.4444448E+07g/s',
                       'Run time': '0904UTC 20/07/2018',
                       'Species': 'VOLCANIC_ASH',
                       'Species Category': 'VOLCANIC',
                       'Start of release': '0000UTC 17/04/2010',
                       'Title': 'VA_Tutorial',
                       'Conventions': 'CF-1.5',
                       'Quantity': 'Air Concentration',
                       'Time Av or Int': '003 hr time averaged',
                       'model_run_title': 'VA_Tutorial',
                       'quantity': 'Air Concentration'},
        'plots': {
            '00500':
                 {'20100418030000': 'VA_Tutorial_Air_Concentration_00500_20100418030000.png',
                  '20100418060000': 'VA_Tutorial_Air_Concentration_00500_20100418060000.png'},
            '01000':
                 {'20100418030000': 'VA_Tutorial_Air_Concentration_01000_20100418030000.png',
                  '20100418060000': 'VA_Tutorial_Air_Concentration_01000_20100418060000.png'}
                  }
        }
    metadata = plot_4d_cube(cube, tmpdir)

    plot_files = [Path(entry).relative_to(tmpdir).as_posix()
                  for entry in scantree(tmpdir) if entry.is_file()]

    assert metadata == expected_metadata
    assert set(plot_files) == set(expected)


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

    assert set(plot_files) == set(expected)


def test_plot_3d_vmax_and_bbox_inches(name_model_result, tmpdir):
    """
    Check that **kwargs are passed to called functions. Only check that they
    haven't caused a crash - visual check determines if they worked
    """
    cube = name_model_result.total_deposition
    expected = ['VA_Tutorial_Total_Deposition_20100418030000.png',
                'VA_Tutorial_Total_Deposition_20100418060000.png']

    plot_3d_cube(cube, tmpdir, vmax=cube.data.max(), bbox_inches='tight')
    plot_files = os.listdir(tmpdir)

    assert set(plot_files) == set(expected)


def test_plot_3d_happy_path(name_model_result, tmpdir):
    cube = name_model_result.total_deposition
    expected = ['VA_Tutorial_Total_Deposition_20100418030000.png',
                'VA_Tutorial_Total_Deposition_20100418060000.png']
    expected_metadata = {
        'created_by': 'plot_3d_cube',
        'attributes': {'End of release': '0800UTC 17/04/2010',
                       'Forecast duration': '75 hours',
                       'Met data': 'NWP Flow.ECMWF ERAInt Regional',
                       'NAME Version': 'NAME III (version 7.2)',
                       'Release height': '1651.000 to 6151.000m asl',
                       'Release location': '19.3600W   63.3700N',
                       'Release rate': '9.4444448E+07g/s',
                       'Run time': '0904UTC 20/07/2018',
                       'Species': 'VOLCANIC_ASH',
                       'Species Category': 'VOLCANIC',
                       'Start of release': '0000UTC 17/04/2010',
                       'Title': 'VA_Tutorial',
                       'Conventions': 'CF-1.5',
                       'Quantity': 'Total deposition',
                       'Time Av or Int': '078 hr time integrated',
                       'model_run_title': 'VA_Tutorial',
                       'quantity': 'Total Deposition'},
        'plots': {'20100418030000': 'VA_Tutorial_Total_Deposition_20100418030000.png',
                  '20100418060000': 'VA_Tutorial_Total_Deposition_20100418060000.png'}}

    metadata = plot_3d_cube(cube, tmpdir)
    plot_files = os.listdir(tmpdir)

    assert metadata == expected_metadata
    assert set(plot_files) == set(expected)


def test_plot_2d_happy_path(name_model_result):
    cube = name_model_result.air_concentration[0, 0, :, :]
    fig, title = draw_2d_cube(cube)

    assert isinstance(fig, Figure)
    assert title == 'VA_Tutorial_Air_Concentration_00500_20100418030000'


def test_plot_2d_no_altitude(name_model_result):
    cube = name_model_result.total_deposition[0, :, :]
    fig, title = draw_2d_cube(cube)

    assert isinstance(fig, Figure)
    assert title == 'VA_Tutorial_Total_Deposition_20100418030000'
