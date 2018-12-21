import os
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


@pytest.fixture(scope='function')
def name_model_result(data_dir):
    """An AshModelResult based on NAME test data."""
    return AshModelResult(data_dir.joinpath('VA_Tutorial_NAME_output.nc'))


@pytest.fixture(scope='module')
def scantree():
    """
    Return a function to recursively yield DirEntry objects for a given
    directory.
    """
    def _scantree(path):
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from _scantree(entry.path)
            else:
                yield entry
    return _scantree
