import logging
from os import listdir
from pathlib import Path
import subprocess

from netCDF4 import Dataset
import pytest

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# pylint: disable=unused-argument, missing-docstring


@pytest.mark.parametrize(
    'results_file, model_type, expected', [
        ('VA_Tutorial_NAME_output.nc', 'name', {
            'VA_Tutorial_Air_Concentration_summary.html',
            'VA_Tutorial_Total_Column_Mass_summary.html',
            'VA_Tutorial_Total_Deposition_summary.html'}),
        ('fall3d_operational.nc', 'fall3d', {
            'Air_Concentration_summary.html',
            'Total_Column_Mass_summary.html',
            'Total_Deposition_summary.html'}),
        ('hysplit_operational.nc', 'hysplit', {
            'Air_Concentration_summary.html',
            'Total_Column_Mass_summary.html',
            'Total_Deposition_summary.html'}),
        ])
def test_plot_ash_model_results_model_types(tmpdir, data_dir, script_dir,
                                            results_file, model_type, expected,
                                            scantree):
    """Test that plotting script works for all data types."""
    # Use set for output files to make order unimportant
    # only check HTML files - assume rest is correct from unit tests
    # Arrange
    script_path = script_dir / 'plot_ash_model_results.py'
    input_file = data_dir / results_file
    model_type = model_type

    # Act
    exit_code = subprocess.check_call(
        ['python', script_path, input_file, '--model_type', model_type,
         '--limits', '-10', '55', '1.1', '70', '--output_dir', tmpdir])
    output_files = {Path(entry).relative_to(tmpdir).as_posix()
                    for entry in scantree(tmpdir) if entry.is_file()}

    # Copy out results for inspection
    logger.debug(f"Test plots in {tmpdir}")

    # Assert
    assert exit_code == 0
    assert expected.issubset(output_files)


def test_plot_ash_model_results_happy_path(tmpdir, data_dir, script_dir,
                                           scantree):
    # Arrange
    script_path = script_dir / 'plot_ash_model_results.py'
    input_file = data_dir / 'VA_Tutorial_NAME_output.nc'
    # Use set for output files to make order unimportant
    expected_output_files = {
        '00500/VA_Tutorial_Air_Concentration_00500_20100418030000.png',
        '00500/VA_Tutorial_Air_Concentration_00500_20100418060000.png',
        '01000/VA_Tutorial_Air_Concentration_01000_20100418030000.png',
        '01000/VA_Tutorial_Air_Concentration_01000_20100418060000.png',
        'VA_Tutorial_Total_Column_Mass_20100418030000.png',
        'VA_Tutorial_Total_Column_Mass_20100418060000.png',
        'VA_Tutorial_Total_Deposition_20100418030000.png',
        'VA_Tutorial_Total_Deposition_20100418060000.png',
        'VA_Tutorial_Air_Concentration_summary.html',
        'VA_Tutorial_Total_Column_Mass_summary.html',
        'VA_Tutorial_Total_Deposition_summary.html',
    }

    # Act
    exit_code = subprocess.check_call(
        ['python', script_path, input_file, '--output_dir', tmpdir])
    output_files = {Path(entry).relative_to(tmpdir).as_posix()
                    for entry in scantree(tmpdir) if entry.is_file()}

    # Copy out results for inspection
    logger.debug(f"Test plots in {tmpdir}")

    # Assert
    assert exit_code == 0
    assert output_files == expected_output_files


def test_plot_ash_model_results_create_dir(tmpdir, data_dir, script_dir,
                                           scantree):
    # Arrange
    script_path = script_dir / 'plot_ash_model_results.py'
    input_file = data_dir / 'VA_Tutorial_NAME_output.nc'
    # Use set for output files to make order unimportant
    expected_output_files = {
        'newdir/00500/VA_Tutorial_Air_Concentration_00500_20100418030000.png',
        'newdir/00500/VA_Tutorial_Air_Concentration_00500_20100418060000.png',
        'newdir/01000/VA_Tutorial_Air_Concentration_01000_20100418030000.png',
        'newdir/01000/VA_Tutorial_Air_Concentration_01000_20100418060000.png',
        'newdir/VA_Tutorial_Total_Column_Mass_20100418030000.png',
        'newdir/VA_Tutorial_Total_Column_Mass_20100418060000.png',
        'newdir/VA_Tutorial_Total_Deposition_20100418030000.png',
        'newdir/VA_Tutorial_Total_Deposition_20100418060000.png',
        'newdir/VA_Tutorial_Air_Concentration_summary.html',
        'newdir/VA_Tutorial_Total_Column_Mass_summary.html',
        'newdir/VA_Tutorial_Total_Deposition_summary.html',
    }

    # Act
    exit_code = subprocess.check_call(
        ['python', script_path, input_file, '--output_dir', tmpdir / 'newdir'])
    output_files = {Path(entry).relative_to(tmpdir).as_posix()
                    for entry in scantree(tmpdir) if entry.is_file()}

    # Copy out results for inspection
    logger.debug(f"Test plots in {tmpdir}")

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
