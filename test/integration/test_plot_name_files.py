import logging
from os import scandir
from pathlib import Path
import subprocess

import pytest

logging.basicConfig(level=logging.DEBUG)

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
    logging.debug(f"Test plots in {plot_dir}")

    # Assert
    assert exit_code == 0
    assert output_files == expected_output_files
