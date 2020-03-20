"""Tests for AshModelResult abstract base class"""
import pytest
from ash_model_plotting import AshModelResult

# pylint: disable=unused-argument, missing-docstring


def test_base_class_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AshModelResult([])


def test_base_class_requires_abstractmethod_definitions():
    class TestAshModelResult(AshModelResult):
        def __repr__(self):
            pass

        def _load_cubes(self):
            pass

        def air_concentration(self):
            pass

        def total_deposition(self):
            pass

        def total_column(self):
            pass

    assert isinstance(TestAshModelResult([]), AshModelResult)
