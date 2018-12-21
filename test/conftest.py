from pathlib import Path

import pytest

from ash_model_plotting.ash_model_result import AshModelResult


@pytest.fixture(scope='module')
def script_dir():
    """Path to the plot_name_files.py script"""
    return Path.cwd().joinpath('ash_model_plotting')


@pytest.fixture(scope='module')
def data_dir():
    """Path to test data files"""
    return Path.cwd().joinpath('test', 'data')


@pytest.fixture(scope='module')
def name_model_result(data_dir):
    """An AshModelResult based on NAME test data."""
    return AshModelResult(data_dir.joinpath('VA_Tutorial_NAME_output.nc'))
