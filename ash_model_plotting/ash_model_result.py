# coding: utf-8
from pathlib import Path

import iris
from netCDF4 import Dataset

from ash_model_plotting.plotting import (
    plot_3d_cube,
    plot_4d_cube,
    render_html,
)


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

    def plot_air_concentration(self, output_dir, file_ext='png',
                               html=True, **kwargs):
        """
        Plot air concentration data to output directory.

        See plotting.plot_4d_cube for details.

        :param output_dir: Target directory for plots
        :param file_ext: File extension
        :param html: bool, set whether html page is created or not
        """
        cube = self.air_concentration

        if not cube:
            msg = 'AshModelResult has no air concentration data'
            raise AshModelResultError(msg)

        metadata = plot_4d_cube(
            cube, output_dir, file_ext=file_ext,
            vmin=0, vmax=cube.data.max(), **kwargs)

        if html:
            self._write_html(output_dir, metadata)

    def plot_total_column(self, output_dir, file_ext='png',
                          html=True, **kwargs):
        """
        Plot total column data to output directory.

        See plotting.plot_3d_cube for details.

        :param output_dir: Target directory for plots
        :param file_ext: File extension
        :param html: bool, set whether html page is created or not
        """
        cube = self.total_column

        if not cube:
            msg = 'AshModelResult has no total column data'
            raise AshModelResultError(msg)

        metadata = plot_3d_cube(
            cube, output_dir, file_ext=file_ext,
            vmin=0, vmax=cube.data.max(), **kwargs)

        if html:
            self._write_html(output_dir, metadata)

    def plot_total_deposition(self, output_dir, file_ext='png',
                              html=True, **kwargs):
        """
        Plot total column data to output directory.

        See plotting.plot_3d_cube for details.

        :param output_dir: Target directory for plots
        :param file_ext: File extension
        :param html: bool, set whether html page is created or not
        """
        cube = self.total_deposition

        if not cube:
            msg = 'AshModelResult has no total deposition data'
            raise AshModelResultError(msg)

        metadata = plot_3d_cube(
            cube, output_dir, file_ext=file_ext,
            vmin=0, vmax=cube.data.max(), **kwargs)

        if html:
            self._write_html(output_dir, metadata)

    def __repr__(self):
        return f"AshModelResult({self.source_file})"

    def _write_html(self, output_dir, metadata):
        """
        Write HTML page for plots using metadata outputs from plotting
        functions.

        :param output_dir: str, target directory for html file
        :param metadata: dict, metadata produced by plot function
        """
        # Prepare HTML
        html = render_html(self.source_file, metadata)

        # Write to file
        name = (f"{metadata['attributes']['Title']}_"
                f"{metadata['attributes']['Quantity']}.html").replace(' ', '_')
        output_file = Path(output_dir) / name
        output_file.write_text(html)
