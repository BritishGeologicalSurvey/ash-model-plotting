import logging
from os import scandir, listdir
from pathlib import Path
import subprocess

import pytest
from netCDF4 import Dataset

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


@pytest.fixture
def script_dir():
    """Path to the plot_name_files.py script"""
    return Path.cwd().joinpath('ash_model_plotting')


@pytest.fixture
def data_dir():
    """Path to test data files"""
    return Path.cwd().joinpath('test', 'data')


def scantree(path):
    """
    Recursively yield DirEntry objects for a given directory.
    """
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry


def test_plot_name_files_air_conc_file(tmpdir, script_dir, data_dir):
    # Arrange
    tmpdir = Path(tmpdir)
    plot_dir = tmpdir / 'plots'
    script_path = script_dir / 'plot_name_files.py'
    expected_output_files = [
        '01000/VA_Tutorial_Air_Concentration_01000_20100418030000.png',
        '01000/VA_Tutorial_Air_Concentration_01000_20100418060000.png',
        '00500/VA_Tutorial_Air_Concentration_00500_20100418030000.png',
        '00500/VA_Tutorial_Air_Concentration_00500_20100418060000.png',
    ]

    # Act
    exit_code = subprocess.check_call(
        ['python', script_path, data_dir, 'Air_Conc', '--output_dir', tmpdir])
    output_files = [Path(entry).relative_to(plot_dir).as_posix()
                    for entry in scantree(plot_dir) if entry.is_file()]

    # Copy out results for inspection
    logger.debug(f"Test plots in {plot_dir}")

    # Assert
    assert exit_code == 0
    assert output_files == expected_output_files


def test_name_to_netcdf_defaults(tmpdir, script_dir, data_dir):
    """
    A very minimal test that checks if script runs and produces an output
    file with correct attributes.
    """
    tmpdir = Path(tmpdir)
    script_path = script_dir / 'name_to_netcdf.py'
    expected_output_file = 'VA_Tutorial_NAME_output.nc'
    expected_variables = [
        'volcanic_ash_air_concentration', 'latitude_longitude', 'time',
        'time_bnds', 'latitude', 'latitude_bnds', 'longitude',
        'longitude_bnds', 'z', 'volcanic_ash_air_concentration_0', 'altitude',
        'altitude_bnds', 'volcanic_ash_total_deposition', 'time_0',
        'time_0_bnds', 'z_0', 'volcanic_ash_dosage', 'z_1']

    # Act
    exit_code = subprocess.check_call(
        ['python', script_path, data_dir, '--output_dir', tmpdir])
    output_file = tmpdir / listdir(tmpdir)[0]

    # Copy out results for inspection
    logger.debug(f"Test output file in {tmpdir}")

    # Assert

    assert exit_code == 0
    assert output_file.name == expected_output_file

    nc = Dataset(output_file.absolute())
    assert expected_variables == list(nc.variables.keys())
