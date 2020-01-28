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


class NameAshModelResult(AshModelResult):
    """
    AshModelResult for data from NAME model simulations.
    """
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

    @property
    def air_concentration(self):
        """
        Cube containing air concentration data
        :return: iris.cube.Cube
        """
        air_concentration = iris.Constraint(
            name='VOLCANIC_ASH_AIR_CONCENTRATION'
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
            name='VOLCANIC_ASH_DOSAGE'
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
            name='VOLCANIC_ASH_TOTAL_DEPOSITION'
        )

        valid_cubes = self.cubes.extract(total_deposition)
        try:
            return valid_cubes.concatenate_cube()
        except ValueError:
            # Return None if no cubes present
            return
