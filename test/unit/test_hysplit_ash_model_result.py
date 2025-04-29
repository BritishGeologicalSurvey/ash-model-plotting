"""Tests for HysplitAshModelResult class."""
from pathlib import Path

from cf_units import Unit
import numpy as np
import pytest
import iris.cube

from ash_model_plotting.ash_model_results import (
    HysplitAshModelResult,
    AshModelResultError,
)

# pylint: disable=unused-argument, missing-docstring


def test_hysplit_ash_model_result_init_happy_path_netcdf(data_dir):
    source_file = data_dir / 'hysplit_operational.nc'
    result = HysplitAshModelResult(source_file)

    assert result.source_data == source_file
    assert isinstance(result.cubes, iris.cube.CubeList)


def test_hysplit_ash_model_result_init_not_a_file():
    with pytest.raises(AshModelResultError):
        HysplitAshModelResult('not a file')


def test_hysplit_ash_model_air_concentration(data_dir):
    source_file = data_dir / 'hysplit_operational.nc'
    result = HysplitAshModelResult(source_file)

    assert isinstance(result.air_concentration, iris.cube.Cube)
    assert (result.air_concentration.name() ==
            "mass_concentration_of_volcanic_ash_in_air")
    assert result.air_concentration.units == Unit('g/m3')


def test_hysplit_ash_model_air_concentration_180(data_dir):
    source_file = data_dir / 'cdump_sum.nc'
    result = HysplitAshModelResult(source_file)

    assert isinstance(result.air_concentration, iris.cube.Cube)
    assert (result.air_concentration.name() ==
            "mass_concentration_of_volcanic_ash_in_air")
    assert result.air_concentration.units == Unit('g/m3')


def test_hysplit_ash_model_total_deposition(data_dir):
    source_file = data_dir / 'hysplit_operational.nc'
    result = HysplitAshModelResult(source_file)

    assert isinstance(result.total_deposition, iris.cube.Cube)
    assert (result.total_deposition.name() ==
            "surface_volcanic_ash_amount")
    assert result.total_deposition.units == Unit('g/m2')


def test_hysplit_ash_model_total_column(data_dir):
    source_file = data_dir / 'hysplit_operational.nc'
    result = HysplitAshModelResult(source_file)

    assert isinstance(result.total_column, iris.cube.Cube)
    assert (result.total_column.name() ==
            "atmosphere_mass_content_of_volcanic_ash")
    assert result.total_column.units == Unit('g/m2')


# TODO: find where 00750 comes from. and also 00000.
@pytest.mark.parametrize('plot_func, expected', [
    ('plot_air_concentration',
     ['01000/Air_Concentration_01000_20200331000000.png',
      '01000/Air_Concentration_01000_20200331060000.png',
      '02000/Air_Concentration_02000_20200331000000.png',
      '02000/Air_Concentration_02000_20200331060000.png',
      'Air_Concentration_summary.html']),
    ('plot_total_column',
     ['Total_Column_Mass_01500_20200331000000.png',
      'Total_Column_Mass_01500_20200331060000.png',
      'Total_Column_Mass_summary.html']),
    ('plot_total_deposition',
     ['Total_Deposition_00000_20200331000000.png',
      'Total_Deposition_00000_20200331060000.png',
      'Total_Deposition_summary.html'])
    ])
def test_plot_functions(hysplit_model_result, tmpdir, plot_func, expected,
                        scantree):
    # Call the plot function - we expect html to be generated here, too
    getattr(hysplit_model_result, plot_func)(tmpdir, clon=0, serial=True)

    plot_files = [Path(entry).relative_to(tmpdir).as_posix()
                  for entry in scantree(tmpdir) if entry.is_file()]

    assert set(plot_files) == set(expected)


@pytest.mark.parametrize('plot_func, expected', [
    ('plot_air_concentration',
     ['01524/Air_Concentration_01524_20250313070000.png',
      '01524/Air_Concentration_01524_20250313100000.png',
      '01524/Air_Concentration_01524_20250313130000.png',
      '03048/Air_Concentration_03048_20250313070000.png',
      '03048/Air_Concentration_03048_20250313100000.png',
      '03048/Air_Concentration_03048_20250313130000.png',
      'Air_Concentration_summary.html']),
    ('plot_total_column',
     ['Total_Column_Mass_02286_20250313070000.png',
      'Total_Column_Mass_02286_20250313100000.png',
      'Total_Column_Mass_02286_20250313130000.png',
      'Total_Column_Mass_summary.html']),
    ('plot_total_deposition',
     ['Total_Deposition_00000_20250313070000.png',
      'Total_Deposition_00000_20250313100000.png',
      'Total_Deposition_00000_20250313130000.png',
      'Total_Deposition_summary.html'])
    ])
def test_plot_functions_180(hysplit_model_result_180, tmpdir, plot_func, expected,
                            scantree):
    # Call the plot function - we expect html to be generated here, too
    getattr(hysplit_model_result_180, plot_func)(tmpdir, clon=180, serial=True)

    plot_files = [Path(entry).relative_to(tmpdir).as_posix()
                  for entry in scantree(tmpdir) if entry.is_file()]

    assert set(plot_files) == set(expected)


@pytest.mark.parametrize('plot_func', [
    'plot_air_concentration',
    'plot_total_column',
    'plot_total_deposition'
    ])
def test_plot_functions_no_data(hysplit_model_result, tmpdir, plot_func):
    # Remove cubes from data so that none are found
    hysplit_model_result.cubes = iris.cube.CubeList()
    with pytest.raises(AshModelResultError):
        getattr(hysplit_model_result, plot_func)(tmpdir)


def test_calculate_total_column(hysplit_model_result):
    # Arrange
    air_concentration = hysplit_model_result.air_concentration
    air_concentration.data = np.ones(air_concentration.data.shape)
    # Collapse two layers 1000 m thick to get time, lat, lon
    expected = np.ones(air_concentration.data.shape)[:, 0, :, :] * 2 * 1000

    # Act
    total_column = HysplitAshModelResult._calculate_total_column(air_concentration)

    # Assert
    np.testing.assert_array_equal(total_column.data, expected)
