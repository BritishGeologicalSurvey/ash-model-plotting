"""Unit tests for plotting module."""
import os
from pathlib import Path

import iris
import matplotlib
from matplotlib.figure import Figure  # noqa
import numpy as np
import pytest

from ash_model_plotting.plotting import (
    plot_2d_cube, plot_3d_cube, plot_4d_cube
)

# pylint: disable=unused-argument, missing-docstring


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
                       'CF Standard Name': 'mass_concentration_of_volcanic_ash_in_air',
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


def test_plot_4d_vmax_and_kwargs(name_model_result, tmpdir, scantree):
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

    plot_4d_cube(cube, tmpdir, vmax=cube.data.max(), bbox_inches='tight',
                 vaac_colours=True)

    plot_files = [Path(entry).relative_to(tmpdir).as_posix()
                  for entry in scantree(tmpdir) if entry.is_file()]

    assert set(plot_files) == set(expected)


def test_plot_3d_vmax_and_kwargs(name_model_result, tmpdir):
    """
    Check that **kwargs are passed to called functions. Only check that they
    haven't caused a crash - visual check determines if they worked
    """
    cube = name_model_result.total_deposition
    expected = ['VA_Tutorial_Total_Deposition_20100418030000.png',
                'VA_Tutorial_Total_Deposition_20100418060000.png']

    plot_3d_cube(cube, tmpdir, vmax=cube.data.max(), bbox_inches='tight',
                 vaac_colours=False)
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
                       'CF Standard Name': 'surface_volcanic_ash_amount',
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
    fig, title = plot_2d_cube(cube)

    assert isinstance(fig, Figure)
    assert title == 'VA_Tutorial_Air_Concentration_00500_20100418030000'


def test_plot_2d_no_altitude(name_model_result):
    cube = name_model_result.total_deposition[0, :, :]
    fig, title = plot_2d_cube(cube)

    assert isinstance(fig, Figure)
    assert title == 'VA_Tutorial_Total_Deposition_20100418030000'


@pytest.mark.parametrize('vaac_colours, expected_cmap', [
    (True, 'from_list'),  # from_list is name for manually defined cmap
    (False, 'viridis'),
    ])
def test_plot_2d_vaac_colours(name_model_result, vaac_colours, expected_cmap):
    # Arrange
    cube = name_model_result.air_concentration[0, 0, :, :]

    # Act
    fig, title = plot_2d_cube(cube, vaac_colours=vaac_colours)
    mesh = [c for c in fig.axes[0].get_children()
            if isinstance(c, matplotlib.collections.QuadMesh)][0]
    cmap = mesh.get_cmap().name

    # Assert
    assert cmap == expected_cmap


@pytest.mark.parametrize('limits, expected_limits', [
    (None, (-80.0, 20.0, 40.0, 80.0)),
    ((-20, 20, 30, 70), (-20, 20, 30, 70)),
    ])
def test_plot_2d_limits(name_model_result, limits, expected_limits):
    # Arrange
    cube = name_model_result.air_concentration[0, 0, :, :]

    # Act
    fig, title = plot_2d_cube(cube, limits=limits)
    geoax = fig.axes[0]
    xlim, ylim = geoax.get_xlim(), geoax.get_ylim()
    limits = (xlim[0], ylim[0], xlim[1], ylim[1])

    # Assert
    assert limits == expected_limits


def test_zlevel_names(name_model_result):
    # Prepare dummy cube
    test_cube = iris.cube.Cube(np.zeros((3, 41, 41)))
    lonlat_cs = iris.coord_systems.GeogCS(6371229)
    fl = iris.coords.DimCoord(
        np.array([100., 275., 450.]),
        bounds=np.array([[0., 200.],
                         [200., 350.],
                         [350., 550.]]),
        long_name='flight_level')
    test_cube.add_dim_coord(fl, 0)
    lon_points = -180 + 4.5 * np.arange(41, dtype=np.float32)
    lat_points = -90 + 4.5 * np.arange(41, dtype=np.float32)
    test_cube.add_dim_coord(
        iris.coords.DimCoord(
            lon_points, "longitude", units="degrees", coord_system=lonlat_cs,
        ),
        1,
    )
    test_cube.add_dim_coord(
        iris.coords.DimCoord(
            lat_points, "latitude", units="degrees", coord_system=lonlat_cs
        ),
        2,
    )
    test_cube.attributes.update(dict(
        model_run_title='Test Cube',
        quantity='my quantity'
    ))

    # Act - plot the first slice
    cube = next(test_cube.slices_over("flight_level"))
    fig, title = plot_2d_cube(cube)

    # Assert
    assert isinstance(fig, Figure)
    assert title == 'Test_Cube_my_quantity_FL000-200'
