"""Tests for REFIR analysis scripts."""
import datetime as dt
import pytest

from ash_model_plotting.analyse_refir_outputs import (
    advisory_area,
    max_concentration_data
)


def test_advisory_area(refir_result):
    data = advisory_area(refir_result)
    expected = {'flight_level': 450.0,
                'time': dt.datetime(2010, 5, 6, 18, 0),
                'advisory_area': 193443000287.01135}
    # Test non-numeric keys
    assert data.pop('time') == expected.pop('time')
    # Test remaining keys
    assert data == pytest.approx(expected)


def test_max_concentration_data(refir_result):
    data = max_concentration_data(refir_result)
    expected = {'flight_level': 100.0,
                'time': dt.datetime(2010, 5, 6, 0, 0),
                'max_concentration': 0.12511915}
    # Test non-numeric keys
    assert data.pop('time') == expected.pop('time')
    # Test remaining keys
    assert data == pytest.approx(expected)
