from os import scandir
from pathlib import Path
import subprocess

import pytest

@pytest.fixture
def script_path():
    """Path to the plot_name_files.py script"""
    return Path.cwd().joinpath('ash-model-plotting', 'plot_name_files.py')


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


def test_plot_name_files_air_conc_file(tmpdir, script_path, data_dir):
    # Arrange
    tmpdir = Path(tmpdir)
    plot_dir = tmpdir / 'plots'
    expected_output_files = [
        '01000/VA_Tutorial_Air_Concentration_01000_20100418030000.png',
        '00500/VA_Tutorial_Air_Concentration_00500_20100418030000.png',
        '04000/VA_Tutorial_Air_Concentration_04000_20100418030000.png',
        '03500/VA_Tutorial_Air_Concentration_03500_20100418030000.png',
        '10500/VA_Tutorial_Air_Concentration_10500_20100418030000.png',
        '04500/VA_Tutorial_Air_Concentration_04500_20100418030000.png',
        '11000/VA_Tutorial_Air_Concentration_11000_20100418030000.png',
        '13000/VA_Tutorial_Air_Concentration_13000_20100418030000.png',
        '02500/VA_Tutorial_Air_Concentration_02500_20100418030000.png',
        '09500/VA_Tutorial_Air_Concentration_09500_20100418030000.png',
        '07000/VA_Tutorial_Air_Concentration_07000_20100418030000.png',
        '07500/VA_Tutorial_Air_Concentration_07500_20100418030000.png',
        '14000/VA_Tutorial_Air_Concentration_14000_20100418030000.png',
        '02000/VA_Tutorial_Air_Concentration_02000_20100418030000.png',
        '12000/VA_Tutorial_Air_Concentration_12000_20100418030000.png',
        '05000/VA_Tutorial_Air_Concentration_05000_20100418030000.png',
        '01500/VA_Tutorial_Air_Concentration_01500_20100418030000.png',
        '08500/VA_Tutorial_Air_Concentration_08500_20100418030000.png',
        '08000/VA_Tutorial_Air_Concentration_08000_20100418030000.png',
        '09000/VA_Tutorial_Air_Concentration_09000_20100418030000.png',
        '05500/VA_Tutorial_Air_Concentration_05500_20100418030000.png',
        '10000/VA_Tutorial_Air_Concentration_10000_20100418030000.png',
        '06000/VA_Tutorial_Air_Concentration_06000_20100418030000.png',
        '12500/VA_Tutorial_Air_Concentration_12500_20100418030000.png',
        '06500/VA_Tutorial_Air_Concentration_06500_20100418030000.png',
        '03000/VA_Tutorial_Air_Concentration_03000_20100418030000.png',
        '13500/VA_Tutorial_Air_Concentration_13500_20100418030000.png',
        '11500/VA_Tutorial_Air_Concentration_11500_20100418030000.png',
        '14500/VA_Tutorial_Air_Concentration_14500_20100418030000.png',
    ]

    # Act
    exit_code = subprocess.check_call(
        ['python', script_path, data_dir, 'Air_Conc', '--output_dir', tmpdir])
    output_files = [Path(entry).relative_to(plot_dir).as_posix()
                    for entry in scantree(plot_dir) if entry.is_file()]

    # Assert
    assert exit_code == 0
    assert output_files == expected_output_files
