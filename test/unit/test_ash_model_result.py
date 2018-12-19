import pytest
import iris.cube

from ash_model_plotting.ash_model_result import (
    AshModelResult,
    AshModelResultError,
)


def test_ash_model_result_init_happy_path(data_dir):
    source_file = data_dir / 'VA_Tutorial_NAME_output.nc'
    result = AshModelResult(source_file)

    assert result.source_file == source_file
    assert isinstance(result.cubes, iris.cube.CubeList)


def test_ash_model_result_init_not_a_file():
    with pytest.raises(AshModelResultError):
        AshModelResult('not a file')


def test_ash_model_result_init_not_netcdf(data_dir):
    source_file = data_dir / 'Air_Conc_grid_201004180300_trimmed.txt'
    with pytest.raises(AshModelResultError):
        AshModelResult(source_file)


def test_ash_model_air_concentration(data_dir):
    source_file = data_dir / 'VA_Tutorial_NAME_output.nc'
    result = AshModelResult(source_file)

    assert isinstance(result.air_concentration, iris.cube.Cube)
    assert result.air_concentration.name() == "VOLCANIC_ASH_AIR_CONCENTRATION"


def test_ash_model_total_deposition(data_dir):
    source_file = data_dir / 'VA_Tutorial_NAME_output.nc'
    result = AshModelResult(source_file)

    assert isinstance(result.total_deposition, iris.cube.Cube)
    assert result.total_deposition.name() == "VOLCANIC_ASH_TOTAL_DEPOSITION"


def test_ash_model_total_column(data_dir):
    source_file = data_dir / 'VA_Tutorial_NAME_output.nc'
    result = AshModelResult(source_file)

    assert isinstance(result.total_column, iris.cube.Cube)
    assert result.total_column.name() == "VOLCANIC_ASH_DOSAGE"
