from pathlib import Path

import pytest


@pytest.fixture
def script_dir():
    """Path to the plot_name_files.py script"""
    return Path.cwd().joinpath('ash_model_plotting')


@pytest.fixture
def data_dir():
    """Path to test data files"""
    return Path.cwd().joinpath('test', 'data')
