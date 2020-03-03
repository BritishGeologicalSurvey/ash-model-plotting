"""
Class to store ash model results.
"""
# coding: utf-8
from pathlib import Path
from warnings import warn

import iris

from ash_model_plotting.ash_model_results import (
    AshModelResult,
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
        self.source_data = Path(self.source_data)
        self._load_from_netcdf()

    @property
    def air_concentration(self):
        """
        Cube containing air concentration data
        :return: iris.cube.Cube
        """
        air_concentration = iris.Constraint(
            name='CON'
            )

        has_zlevel = iris.Constraint(cube_func=self._has_zlevels)

        try:
            valid_cubes = self.cubes.extract(air_concentration & has_zlevel)
            cube = valid_cubes.concatenate_cube()
            cube.attributes['model_run_title'] = self._get_model_run_title(cube)
            cube.attributes['quantity'] = 'Air Concentration'
            if cube.attributes['units'] == "gr/m3":
                warn("Air concentration reports units of"
                     "\"gr/m3\", which represents *grains* in"
                     " the udunits library. This may cause issues"
                     " in unit conversion. \n"
                     "(Did you mean \"g/m3\")")

            return cube
        except ValueError:
            # Return None if no cubes present
            # A warning might be useful here?
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
            name='LOAD'
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
