from pathlib import Path

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


@pytest.mark.parametrize('plot_func, expected', [
    ('plot_air_concentration', [
      '01000/VA_Tutorial_Air_Concentration_01000_20100418030000.png',
      '01000/VA_Tutorial_Air_Concentration_01000_20100418060000.png',
      '00500/VA_Tutorial_Air_Concentration_00500_20100418030000.png',
      '00500/VA_Tutorial_Air_Concentration_00500_20100418060000.png']),
    ('plot_total_column', [
      'VA_Tutorial_Dosage_20100418030000.png',
      'VA_Tutorial_Dosage_20100418060000.png']),
    ('plot_total_deposition', [
      'VA_Tutorial_Total_deposition_20100418030000.png',
      'VA_Tutorial_Total_deposition_20100418060000.png'])
    ])
def test_plot_functions(name_model_result, tmpdir, plot_func, expected,
                        scantree):
    # Call the plot function
    getattr(name_model_result, plot_func)(tmpdir)

    plot_files = [Path(entry).relative_to(tmpdir).as_posix()
                  for entry in scantree(tmpdir) if entry.is_file()]

    assert plot_files == expected


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
