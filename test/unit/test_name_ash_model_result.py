"""Tests for NameAshModelResult class."""
from pathlib import Path

import pytest
import iris.cube

from ash_model_plotting.ash_model_results import (
    NameAshModelResult,
    AshModelResultError,
)

# pylint: disable=unused-argument, missing-docstring


def test_name_ash_model_result_init_happy_path_netcdf(data_dir):
    source_file = data_dir / 'VA_Tutorial_NAME_output.nc'
    result = NameAshModelResult(source_file)

    assert result.source_data == source_file
    assert isinstance(result.cubes, iris.cube.CubeList)


def test_name_ash_model_result_init_happy_path_name_format(data_dir):
    source_files = [str(f) for f in data_dir.glob('*.txt')]
    result = NameAshModelResult(source_files)

    assert result.source_data == source_files
    assert isinstance(result.cubes, iris.cube.CubeList)


def test_name_ash_model_result_single_file_input(data_dir):
    source_file = data_dir / 'Air_Conc_grid_201004180300_trimmed.txt'
    result = NameAshModelResult(source_file)

    assert result.source_data == source_file
    assert isinstance(result.cubes, iris.cube.CubeList)


def test_name_ash_model_result_init_not_a_file():
    with pytest.raises(AshModelResultError):
        NameAshModelResult('not a file')


def test_name_ash_model_air_concentration(data_dir):
    source_file = data_dir / 'VA_Tutorial_NAME_output.nc'
    result = NameAshModelResult(source_file)

    assert isinstance(result.air_concentration, iris.cube.Cube)
    assert result.air_concentration.name() == "VOLCANIC_ASH_AIR_CONCENTRATION"


def test_name_ash_model_total_deposition(data_dir):
    source_file = data_dir / 'VA_Tutorial_NAME_output.nc'
    result = NameAshModelResult(source_file)

    assert isinstance(result.total_deposition, iris.cube.Cube)
    assert result.total_deposition.name() == "VOLCANIC_ASH_TOTAL_DEPOSITION"


def test_name_ash_model_total_column(data_dir):
    source_file = data_dir / 'VA_Tutorial_NAME_output.nc'
    result = NameAshModelResult(source_file)

    assert isinstance(result.total_column, iris.cube.Cube)
    assert result.total_column.name() == "VOLCANIC_ASH_DOSAGE"


@pytest.mark.parametrize('plot_func, expected', [
    ('plot_air_concentration',
     ['01000/VA_Tutorial_Air_Concentration_01000_20100418030000.png',
      '01000/VA_Tutorial_Air_Concentration_01000_20100418060000.png',
      '00500/VA_Tutorial_Air_Concentration_00500_20100418030000.png',
      '00500/VA_Tutorial_Air_Concentration_00500_20100418060000.png',
      'VA_Tutorial_Air_Concentration_summary.html']),
    ('plot_total_column',
     ['VA_Tutorial_Total_Column_Mass_20100418030000.png',
      'VA_Tutorial_Total_Column_Mass_20100418060000.png',
      'VA_Tutorial_Total_Column_Mass_summary.html']),
    ('plot_total_deposition',
     ['VA_Tutorial_Total_Deposition_20100418030000.png',
      'VA_Tutorial_Total_Deposition_20100418060000.png',
      'VA_Tutorial_Total_Deposition_summary.html'])
    ])
def test_plot_functions(name_model_result, tmpdir, plot_func, expected,
                        scantree):
    # Call the plot function - we expect html to be generated here, too
    getattr(name_model_result, plot_func)(tmpdir)

    plot_files = [Path(entry).relative_to(tmpdir).as_posix()
                  for entry in scantree(tmpdir) if entry.is_file()]

    assert set(plot_files) == set(expected)


def test_plot_air_concentration_single_file(data_dir, tmpdir, scantree):
    name_model_result = NameAshModelResult(
        data_dir / "Air_Conc_grid_201004180300_trimmed.txt")
    name_model_result.plot_air_concentration(tmpdir)
    expected = ['VA_Tutorial_Air_Concentration_summary.html',
                'VA_Tutorial_Air_Concentration_01000_20100418030000.png',
                'VA_Tutorial_Air_Concentration_00500_20100418030000.png']

    plot_files = [Path(entry).relative_to(tmpdir).as_posix()
                  for entry in scantree(tmpdir) if entry.is_file()]

    assert set(plot_files) == set(expected)


@pytest.mark.parametrize('plot_func', [
    'plot_air_concentration',
    'plot_total_column',
    'plot_total_deposition'
    ])
def test_plot_functions_no_data(name_model_result, tmpdir, plot_func):
    # Call the plot function
    name_model_result.cubes = iris.cube.CubeList()
    with pytest.raises(AshModelResultError):
        getattr(name_model_result, plot_func)(tmpdir)
