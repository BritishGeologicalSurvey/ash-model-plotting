"""Tests for zlevel switching in plotting module."""
from collections import namedtuple
import pytest

from ash_model_plotting.plotting import (
    _get_zlevels
)


def test_get_zlevels_altitude(name_model_result):
    cube = name_model_result.air_concentration
    expected = [500.0, 1000.0]
    levels = _get_zlevels(cube)

    assert levels == expected


def test_get_zlevels_flight_level(refir_result):
    cube = refir_result.cubes[0]
    expected = [100.0, 275.0, 450.0]
    levels = _get_zlevels(cube)

    assert levels == expected


def test_get_zlevels_bad_cube_shape():
    # Arrange - create mock with coords method that returns length 2 item
    MockCube = namedtuple('MockCube', 'coords')
    mock_cube = MockCube(lambda: [1, 2])

    # Act and assert
    with pytest.raises(ValueError):
        _get_zlevels(mock_cube)
