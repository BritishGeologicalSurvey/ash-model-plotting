"""Test fixtures for use with pytest"""
import os
from pathlib import Path

import pytest
import matplotlib

from ash_model_plotting import (NameAshModelResult,
                                Fall3DAshModelResult)

# Use Agg plotting backend for tests so matplotlib doesn't open window
matplotlib.use('Agg')


@pytest.fixture(scope='module')
def script_dir():
    """Path to the plot_ash_model_results.py script"""
    return Path.cwd().joinpath('ash_model_plotting')


@pytest.fixture(scope='module')
def data_dir():
    """Path to test data files"""
    return Path.cwd().joinpath('test', 'data')


@pytest.fixture(scope='function')
def name_model_result(data_dir):
    """An NameAshModelResult based on NAME test data."""
    return NameAshModelResult(data_dir.joinpath('VA_Tutorial_NAME_output.nc'))


@pytest.fixture(scope='function')
def refir_result(data_dir):
    """An NameAshModelResult based on NAME test data."""
    refir_files = [str(f.absolute()) for f in data_dir.rglob('REFIR*.txt')]
    return NameAshModelResult(refir_files)


@pytest.fixture(scope='function')
def fall3d_model_result(data_dir):
    """An Fall3DAshModelResult based on test data."""
    return Fall3DAshModelResult(data_dir.joinpath('fall3d_realistic_res_clip.nc'))


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
