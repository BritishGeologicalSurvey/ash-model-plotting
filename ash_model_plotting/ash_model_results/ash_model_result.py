"""
Class to store ash model results.
"""
# coding: utf-8
from abc import ABCMeta, abstractmethod
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


class AshModelResult(metaclass=ABCMeta):
    """
    Class to store ash model results with plotting methods
    """
    _air_concentration_names = set()
    _total_deposition_names = set()
    _total_column_names = set()
    _zlevel_names = {'altitude', 'alt', 'flight_level',
                     'z coordinate of x-y plane cuts'}

    def __init__(self, source_data):
        self.source_data = source_data
        self._load_cubes()

    @abstractmethod
    def __repr__(self):
        return f"AshModelResult({self.source_data})"

    @abstractmethod
    def _load_cubes(self):
        """
        Load cubes from data files.  Override this to deal with specific
        model data formats.
        """
        pass

    @property
    @abstractmethod
    def air_concentration(self):
        """
        Cube containing air concentration data.  Override to extract specific
        attribute names used by different model formats.
        :return: iris.cube.Cube
        """
        pass

    @property
    @abstractmethod
    def total_column(self):
        """
        Cube containing total_column loading data. Override to extract specific
        attribute names used by different model formats.

        :return: iris.cube.Cube
        """
        pass

    @property
    @abstractmethod
    def total_deposition(self):
        """
        Cube containing total deposition loading data.  Override to extract specific
        attribute names used by different model formats.
        :return: iris.cube.Cube
        """
        pass

    def _has_zlevels(self, cube):
        """
        Determines if a cube has z-levels.

        :return: bool
        """
        coord_names = {c.name() for c in cube.coords()}
        # is_disjoint() is True if sets don't overlap
        return not self._zlevel_names.isdisjoint(coord_names)

    @staticmethod
    def _get_model_run_title(cube):
        """
        Extract pretty formatted run-title name from cube
        attributes.

        :return: str
        """
        # Title, TITLE, (None)
        if 'Title' in cube.attributes:
            title = cube.attributes.get('Title')
        elif 'TITLE' in cube.attributes:
            title = cube.attributes.get('TITLE')
        else:
            title = ''

        return title

    def _load_from_netcdf(self):
        """
        Load cubes from NetCDF4 file with minor error-checking for valid file
        """
        # Check that NetCDF4 driver can open file
        try:
            nc = Dataset(self.source_data)
            nc.close()
        except (OSError, FileNotFoundError) as e:
            msg = (f"{self.source_data.absolute()} is not a valid '"
                   f"NetCDF4 file:\n{e}")
            raise AshModelResultError(msg)

        self.cubes = iris.load(str(self.source_data))

    def plot_air_concentration(self, output_dir, file_ext='png',
                               html=True, vaac_colours=False, **kwargs):
        """
        Plot air concentration data to output directory.

        See plotting.plot_4d_cube for details.

        :param output_dir: Target directory for plots
        :param file_ext: File extension
        :param html: bool, set whether html page is created or not
        :param vaac_colors: bool, use vaac_colors for plot
        :param kwargs: dict; extra arguments to pass to plot_2d_cube and
            plt.savefig e.g. limits, vaac_colours, dpi, bbox_inches
        """
        kwargs.update(vaac_colours=vaac_colours)
        cube = self.air_concentration

        if not cube:
            msg = 'AshModelResult has no air concentration data'
            raise AshModelResultError(msg)

        if len(cube.data.shape) == 3:
            plot_func = plot_3d_cube
        else:
            plot_func = plot_4d_cube

        metadata = plot_func(
            cube, output_dir, file_ext=file_ext, vmin=0, vmax=cube.data.max(),
            **kwargs)

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
        :param kwargs: dict; extra arguments to pass to plot_2d_cube and
            plt.savefig e.g. limits, vaac_colours, dpi, bbox_inches
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
        :param kwargs: dict; extra arguments to pass to plot_2d_cube and
            plt.savefig e.g. limits, vaac_colours, dpi, bbox_inches
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

    def _write_html(self, output_dir, metadata):
        """
        Write HTML page for plots using metadata outputs from plotting
        functions.

        :param output_dir: str, target directory for html file
        :param metadata: dict, metadata produced by plot function
        """
        # Prepare HTML
        html = render_html(self.source_data, metadata)

        # Write to file
        name = '_'.join(filter(None, (
            metadata['attributes'].get('model_run_title'),
            metadata['attributes'].get('quantity'),
            "summary.html"))).replace(' ', '_')
        output_file = Path(output_dir) / name
        output_file.write_text(html)
