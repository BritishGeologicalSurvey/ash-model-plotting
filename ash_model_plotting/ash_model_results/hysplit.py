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


class HysplitAshModelResult(AshModelResult):
    """
    AshModelResult for data from Hysplit model simulations.
    """
    def __repr__(self):
        return f"HysplitAshModelResult({self.source_data})"

    def _load_cubes(self):
        """
        Load cubes from single NetCDF file
        """
        # Load from NetCDF
        source_data = Path(self.source_data)
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
            name='Concentration Array - ASH '
            )

        above_ground = iris.Constraint(
            coord_values={'Top height of each layer': lambda cell: cell > 0})

        try:
            valid_cubes = self.cubes.extract(air_concentration & above_ground)
            cube = valid_cubes.concatenate_cube()
            cube.attributes['model_run_title'] = self._get_model_run_title(cube)
            cube.attributes['quantity'] = 'Air Concentration'
            return cube
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

        try:
            valid_cubes = self.cubes.extract(total_column)
            cube = valid_cubes.concatenate_cube()
            cube.attributes['model_run_title'] = self._get_model_run_title(cube)
            cube.attributes['quantity'] = 'Total Column Mass'
            return cube
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

        try:
            valid_cubes = self.cubes.extract(total_deposition)
            cube = valid_cubes.concatenate_cube()
            cube.attributes['model_run_title'] = self._get_model_run_title(cube)
            cube.attributes['quantity'] = 'Total Deposition'
            return cube
        except ValueError:
            # Return None if no cubes present
            return
