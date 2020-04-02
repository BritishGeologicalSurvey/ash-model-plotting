"""Tests for Fall3DAshModelResult class."""
from pathlib import Path

import pytest
import iris.cube

from ash_model_plotting.ash_model_results import (
    Fall3DAshModelResult,
    AshModelResultError,
)

# pylint: disable=unused-argument, missing-docstring


def test_fall3d_ash_model_result_init_happy_path_netcdf(data_dir):
    source_file = data_dir / 'fall3d_realistic_res_clip.nc'
    result = Fall3DAshModelResult(source_file)

    assert result.source_data == source_file
    assert isinstance(result.cubes, iris.cube.CubeList)


def test_fall3d_ash_model_result_init_not_a_file():
    with pytest.raises(AshModelResultError):
        Fall3DAshModelResult('not a file')


def test_fall3d_ash_model_air_concentration(data_dir):
    source_file = data_dir / 'fall3d_realistic_res_clip.nc'
    result = Fall3DAshModelResult(source_file)

    # Current Fall3D test data has wrong units - this should raise
    # a warning whenever calling air_concentration
    with pytest.warns(UserWarning):
        assert isinstance(result.air_concentration, iris.cube.Cube)
        assert result.air_concentration.name() == "CON"


def test_fall3d_ash_model_total_deposition(data_dir):
    source_file = data_dir / 'fall3d_realistic_res_clip.nc'
    result = Fall3DAshModelResult(source_file)

    assert isinstance(result.total_deposition, iris.cube.Cube)
    assert result.total_deposition.name() == "LOAD"


def test_fall3d_ash_model_total_column(data_dir):
    source_file = data_dir / 'fall3d_realistic_res_clip.nc'
    result = Fall3DAshModelResult(source_file)

    assert isinstance(result.total_column, iris.cube.Cube)
    assert result.total_column.name() == "COL_MASS"


@pytest.mark.parametrize('plot_func, expected', [
    ('plot_air_concentration',
     ['00000/Fall3d_7.1_results_Air_Concentration_00000_20100418030000.png',
      '00000/Fall3d_7.1_results_Air_Concentration_00000_20100418060000.png',
      '01000/Fall3d_7.1_results_Air_Concentration_01000_20100418030000.png',
      '01000/Fall3d_7.1_results_Air_Concentration_01000_20100418060000.png',
      '00500/Fall3d_7.1_results_Air_Concentration_00500_20100418030000.png',
      '00500/Fall3d_7.1_results_Air_Concentration_00500_20100418060000.png',
      'Fall3d_7.1_results_Air_Concentration_summary.html']),
    ('plot_total_column',
     ['Fall3d_7.1_results_Total_Column_Mass_20100418030000.png',
      'Fall3d_7.1_results_Total_Column_Mass_20100418060000.png',
      'Fall3d_7.1_results_Total_Column_Mass_summary.html']),
    ('plot_total_deposition',
     ['Fall3d_7.1_results_Total_Deposition_20100418030000.png',
      'Fall3d_7.1_results_Total_Deposition_20100418060000.png',
      'Fall3d_7.1_results_Total_Deposition_summary.html'])
    ])
def test_plot_functions(fall3d_model_result, tmpdir, plot_func, expected,
                        scantree):
    # Call the plot function - we expect html to be generated here, too
    getattr(fall3d_model_result, plot_func)(tmpdir)

    plot_files = [Path(entry).relative_to(tmpdir).as_posix()
                  for entry in scantree(tmpdir) if entry.is_file()]

    assert set(plot_files) == set(expected)


@pytest.mark.parametrize('plot_func', [
    'plot_air_concentration',
    'plot_total_column',
    'plot_total_deposition'
    ])
def test_plot_functions_no_data(fall3d_model_result, tmpdir, plot_func):
    # Remove cubes from data so that none are found
    fall3d_model_result.cubes = iris.cube.CubeList()
    with pytest.raises(AshModelResultError):
        getattr(fall3d_model_result, plot_func)(tmpdir)
