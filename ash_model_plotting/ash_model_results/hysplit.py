"""
Class to store ash model results.
"""
# coding: utf-8
from pathlib import Path

import iris
import numpy as np

from ash_model_plotting.ash_model_results import (
    AshModelResult,
    AshModelResultError,
)


class HysplitAshModelResult(AshModelResult):
    """
    AshModelResult for data from Hysplit model simulations.
    """
    _air_concentration_names = {
        'Concentration Array - AS01'
    }

    def __repr__(self):
        return f"HysplitAshModelResult({self.source_data})"

    def _load_cubes(self):
        """
        Load cubes from single NetCDF file
        """
        self.source_data = Path(self.source_data)
        self._load_from_netcdf()

    @property
    def air_concentration(self):
        """
        Cube containing air concentration data.
        The lowest altitude in the cube corresponds to deposition.
        :return: iris.cube.Cube
        """
        air_concentration = iris.Constraint(
            cube_func=lambda c: c.name() in self._air_concentration_names
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
        Cube containing total_column loading data.
        For Hysplit data, the total column loading must be calculated
        on-the-fly by summing the mass of volcanic ash at each zlevel.
        :return: iris.cube.Cube
        """
        if self.air_concentration:
            cube = self._calculate_total_column(self.air_concentration)
            cube.attributes['model_run_title'] = self._get_model_run_title(cube)
            cube.attributes['quantity'] = 'Total Column Mass'
            cube.rename("VOLCANIC_ASH_DOSAGE")
            return cube
        else:
            # Return None if no cubes present
            return

    @staticmethod
    def _calculate_total_column(cube):
        """
        Collapse a cube of air_concentration by summing the mass of volcanic ash at each zlevel.
        """
        # Get thicknesses of zlevels
        zlevels = cube.coord('Top height of each layer')
        zlevel_thicknesses = np.concatenate((zlevels.points[:1],
                                             np.diff(zlevels.points)))

        # Setting weights for collapsed cube (should match shape of data array)
        weights = np.ones(cube.data.shape)
        for i, thickness in enumerate(zlevel_thicknesses):
            weights[:, i, :, :] *= thickness

        # Collapsing cube
        return cube.collapsed('Top height of each layer', iris.analysis.SUM,
                              weights=weights)

    @property
    def total_deposition(self):
        """
        Cube containing total deposition loading data
        :return: iris.cube.Cube
        """
        ash_data = iris.Constraint(
            cube_func=lambda c: c.name() in self._air_concentration_names
            )

        ground_level = iris.Constraint(
            coord_values={'Top height of each layer': lambda cell: cell == 0})

        try:
            valid_cubes = self.cubes.extract(ash_data & ground_level)
            cube = valid_cubes.concatenate_cube()
            cube.rename('VOLCANIC_ASH_TOTAL_DEPOSITION')
            cube.attributes['model_run_title'] = self._get_model_run_title(cube)
            cube.attributes['quantity'] = 'Total Deposition'
            # Overwrite data to give cumulative sum (as original is per step)
            cube.data = np.cumsum(cube.data, axis=0)
            return cube
        except ValueError:
            # Return None if no cubes present
            return