"""Tests for REFIR analysis scripts."""
import pytest

from ash_model_plotting.analyse_refir_outputs import (
    max_concentration_data
)


def test_extract_max_air_conc_info(refir_result):
    data = max_concentration_data(refir_result)
    expected = {'flight_level': 100.0,
                'time': 353640.0,
                'max_concentration': 0.12511915}
    assert data == pytest.approx(expected)
