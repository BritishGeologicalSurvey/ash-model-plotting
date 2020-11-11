"""Test fixtures for use with pytest"""
import os
from pathlib import Path

import pytest
import matplotlib

from ash_model_plotting import (NameAshModelResult,  # noqa: E402
                                HysplitAshModelResult,
                                Fall3DAshModelResult)


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
    return Fall3DAshModelResult(data_dir.joinpath('fall3d_operational.nc'))


@pytest.fixture(scope='function')
def hysplit_model_result(data_dir):
    """A HysplitAshModelResult based on test data."""
    return HysplitAshModelResult(data_dir.joinpath('hysplit_operational.nc'))


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
