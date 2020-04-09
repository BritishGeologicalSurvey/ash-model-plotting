"""
Class to store ash model results.
"""
# coding: utf-8
from functools import lru_cache
from pathlib import Path

import iris

from ash_model_plotting.ash_model_results import (
    AshModelResult,
    AshModelResultError,
)


class NameAshModelResult(AshModelResult):
    """
    AshModelResult for data from NAME model simulations.
    """
    _air_concentration_names = {
        'VOLCANIC_ASH_AIR_CONCENTRATION'
    }

    _total_column_names = {
        'VOLCANIC_ASH_DOSAGE'
    }

    _total_deposition_names = {
        'VOLCANIC_ASH_TOTAL_DEPOSITION'
    }

    def __repr__(self):
        return f"NameAshModelResult({self.source_data})"

    def _load_cubes(self):
        """
        Load cubes from single NetCDF file or list of NAME-format .txt files
        """
        # TODO: improve error handling here
        # Load from many NAME files
        if isinstance(self.source_data, list):
            self.cubes = iris.load(self.source_data)
            return

        # Load from NetCDF
        source_data = Path(self.source_data)
        if source_data.suffix.lower() == '.nc':
            self._load_from_netcdf()
        else:
            # Assuming single NAME .txt file
            try:
                self.cubes = iris.load(str(source_data))
            except OSError:
                msg = f"{source_data.absolute()} not found"
                raise AshModelResultError(msg)

    @property  # type: ignore
    @lru_cache(maxsize=1)
    def air_concentration(self):
        """
        Cube containing air concentration data
        :return: iris.cube.Cube
        """
        air_concentration = iris.Constraint(
            cube_func=lambda c: c.name() in self._air_concentration_names
            )

        has_zlevel = iris.Constraint(cube_func=self._has_zlevels)

        try:
            valid_cubes = self.cubes.extract(air_concentration & has_zlevel)
            cube = valid_cubes.concatenate_cube()
            cube.attributes['model_run_title'] = self._get_model_run_title(cube)
            cube.attributes['quantity'] = 'Air Concentration'
            cube.attributes['CF Standard Name'] = (
                "mass_concentration_of_volcanic_ash_in_air")
            return cube
        except ValueError:
            # Return None if no cubes present
            return

    @property  # type: ignore
    @lru_cache(maxsize=1)
    def total_column(self):
        """
        Cube containing total_column loading data
        :return: iris.cube.Cube
        """
        total_column = iris.Constraint(
            cube_func=lambda c: c.name() in self._total_column_names
        )

        try:
            valid_cubes = self.cubes.extract(total_column)
            cube = valid_cubes.concatenate_cube()
            cube.attributes['model_run_title'] = self._get_model_run_title(cube)
            cube.attributes['quantity'] = 'Total Column Mass'
            cube.attributes['CF Standard Name'] = (
                "atmosphere_mass_content_of_volcanic_ash")
            return cube
        except ValueError:
            # Return None if no cubes present
            return

    @property  # type: ignore
    @lru_cache(maxsize=1)
    def total_deposition(self):
        """
        Cube containing total deposition loading data
        :return: iris.cube.Cube
        """
        total_deposition = iris.Constraint(
            cube_func=lambda c: c.name() in self._total_deposition_names
        )

        try:
            valid_cubes = self.cubes.extract(total_deposition)
            cube = valid_cubes.concatenate_cube()
            cube.attributes['model_run_title'] = self._get_model_run_title(cube)
            cube.attributes['quantity'] = 'Total Deposition'
            cube.attributes['CF Standard Name'] = "surface_volcanic_ash_amount"
            return cube
        except ValueError:
            # Return None if no cubes present
            return
