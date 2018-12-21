# coding: utf-8
import os
from pathlib import Path

import iris
import iris.plot as iplt
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np


class AshModelResultError(Exception):
    pass


class AshModelResult(object):
    """
    Class to store ash model results from NetCDF4 file with plotting methods
    """
    def __init__(self, source_file):
        self.source_file = Path(source_file)
        self._load_cubes()

    def _load_cubes(self):
        """
        Load cubes with minor error-checking for valid file
        """
        # Check that NetCDF4 driver can open file
        try:
            nc = Dataset(self.source_file)
            nc.close()
        except (OSError, FileNotFoundError) as e:
            msg = (f"{self.source_file.absolute()} is not a valid '"
                   f"NetCDF4 file:\n{e}")
            raise AshModelResultError(msg)

        self.cubes = iris.load(str(self.source_file))

    @property
    def air_concentration(self):
        """
        Cube containing air concentration data
        :return: iris.cube.Cube
        """
        air_concentration = iris.Constraint(
            name='VOLCANIC_ASH_AIR_CONCENTRATION'
            )

        has_altitude = iris.Constraint(
            cube_func=lambda cube: 'altitude' in {
                c[0].standard_name for c in cube.dim_coords}
        )

        valid_cubes = self.cubes.extract(air_concentration & has_altitude)
        return valid_cubes.concatenate_cube()

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
        return valid_cubes.concatenate_cube()

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
        return valid_cubes.concatenate_cube()

    def plot_air_concentration(self, output_dir):
        """
        Plot air concentration data into directories per level
        :param output_dir:
        """
        # Mask out data below threshold
        cube = self.air_concentration.copy()
        cube.data = np.ma.masked_less(cube.data, 1e-8)

        # Prepare plot directory
        plot_dir = Path(output_dir).joinpath('plots')
        if not os.path.isdir(plot_dir):
            os.mkdir(plot_dir)

        # Plot
        timestamps = cube.coord('time')
        levels = cube.coord('altitude')
        for i, level in enumerate(levels):
            for t, timestamp in enumerate(timestamps):
                print(level, timestamp)
                # Prepare plot directory for given level
                level_name = f'{int(level.points[0]):05d}'  # Get level as text string
                level_plot_dir = os.path.join(plot_dir, level_name)
                if not os.path.isdir(level_plot_dir):
                    os.mkdir(level_plot_dir)

                # Plot map for level
                fig, title = self._draw_figure_for_slice(cube, level, i, t)
                fig.savefig(os.path.join(plot_dir, level_name, title),
                            bbox_inches='tight')
                plt.close(fig)


    def __repr__(self):
        return f"AshModelResult({self.source_file})"

