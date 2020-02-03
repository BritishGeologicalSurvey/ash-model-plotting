"""
Class to store ash model results.
"""
# coding: utf-8
from pathlib import Path

import iris

from ash_model_plotting.ash_model_results import (
    AshModelResult,
    AshModelResultError,
)


class Fall3DAshModelResult(AshModelResult):
    """
    AshModelResult for data from FALL3D model simulations.
    """
    def __repr__(self):
        return f"Fall3DAshModelResult({self.source_data})"

    def _load_cubes(self):
        """
        Load cubes from single NetCDF file
        """
        # Load from NetCDF
        source_data = Path(self.source_data)
        try:
            self._load_from_netcdf()
        except OSError:
            msg = f"{source_data.absolute()} not found"
            raise AshModelResultError(msg)

    @property
    def air_concentration(self):
        """
        Cube containing air concentration data
        :return: iris.cube.Cube
        """
        air_concentration = iris.Constraint(
            name='CON'
            )

        def match_zlevels(cube):
            # is_disjoint() is True if sets don't overlap
            zlevels = {'altitude', 'flight_level'}
            coord_names = {c.name() for c in cube.coords()}
            return not zlevels.isdisjoint(coord_names)

        has_zlevel = iris.Constraint(cube_func=match_zlevels)

        valid_cubes = self.cubes.extract(air_concentration & has_zlevel)
        try:
            return valid_cubes.concatenate_cube()
        except ValueError:
            # Return None if no cubes present
            return

    @property
    def total_column(self):
        """
        Cube containing total_column loading data
        :return: iris.cube.Cube
        """
        total_column = iris.Constraint(
            name='COL_MASS'
        )

        valid_cubes = self.cubes.extract(total_column)
        try:
            return valid_cubes.concatenate_cube()
        except ValueError:
            # Return None if no cubes present
            return

    @property
    def total_deposition(self):
        """
        Cube containing total deposition loading data
        :return: iris.cube.Cube
        """
        total_deposition = iris.Constraint(
            name='LOAD'
        )

        valid_cubes = self.cubes.extract(total_deposition)
        try:
            return valid_cubes.concatenate_cube()
        except ValueError:
            # Return None if no cubes present
            return
