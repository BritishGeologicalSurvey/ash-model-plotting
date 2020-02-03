"""Tests for Fall3DAshModelResult class."""
import pytest
import iris.cube

from ash_model_plotting.ash_model_results import (
    Fall3DAshModelResult,
    AshModelResultError,
)


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
