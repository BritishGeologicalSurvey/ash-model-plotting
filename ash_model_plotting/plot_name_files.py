# coding: utf-8
import argparse
import glob
import logging
import os
from pathlib import Path

import iris
import iris.plot as iplt
import matplotlib.pyplot as plt
import numpy as np

# Monkey patch GeoAxes to fix Matplotlib v3.0.0 - related bug
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
GeoAxes._pcolormesh_patched = Axes.pcolormesh

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def plot_name_files(source_dir, prefix, output_dir):
    """
    Read the files named 'source_dir/prefix*' and generate plots. Files are
    saved with `plots` dir.
    :param source_dir: str, path to directory containing files
    :param prefix: str, common prefix of files to parse
    :param output_dir: str, directory for plot output
    """
    if not output_dir:
        output_dir = source_dir
    logger.info(f'Writing files from {source_dir}/{prefix}* to {output_dir}')

    for source_file in glob.glob(
            str(source_dir.absolute().joinpath(prefix + '*'))):
        logger.debug(f'Plotting data from {source_file}')
        plot_levels(source_file, output_dir)


def plot_levels(source_file, output_dir):
    """
    Plot a single NAME file
    :param source_file:
    :param output_dir:
    """
    # Load data
    cubes = iris.load(source_file)
    # TODO: fix this hack that skips ground-level cube (try concatenating?)
    cube = cubes[1]

    # Mask out data below threshold
    cube.data = np.ma.masked_less(cube.data, 1e-8)

    # Prepare plot directory
    plot_dir = os.path.join(output_dir, 'plots')
    if not os.path.isdir(plot_dir):
        os.mkdir(plot_dir)

    # Plot
    levels = cube.coord('altitude')
    for i, level in enumerate(levels):
        # Prepare plot directory for given level
        level_name = f'{int(level.points[0]):05d}'  # Get level as text string
        logger.debug(f'Plotting level {level_name}')
        level_plot_dir = os.path.join(plot_dir, level_name)
        if not os.path.isdir(level_plot_dir):
            os.mkdir(level_plot_dir)

        # Plot map for level
        fig, title = plot_level(cube, level, i)
        fig.savefig(os.path.join(plot_dir, level_name, title),
                    bbox_inches='tight')
        plt.close(fig)


def plot_level(cube, level, idx):
    """
    Plot a map of an individual level from a data cube
    :param cube: iris Cube with data
    :param level: iris.coord.DimCoord for given level
    :param idx: int, index for given level
    :return fig, name: Matplotlib figure with plot and str with name
    """
    # Plot data
    fig = plt.figure()
    mesh_plot = iplt.pcolormesh(cube[idx, :, :], vmin=0, vmax=cube.data.max())
    ax = plt.gca()
    ax.coastlines(resolution='50m', color='grey')
    ax.grid(True)
    cbar = fig.colorbar(mesh_plot, orientation='horizontal')
    cbar.set_label(f'{cube.long_name.title()} ({cube.units})')

    # Get and set title
    timestamp = cube.coord('time')
    title = "{title}_{quantity}_{level:05d}_{timestamp}.png".format(
        title=cube.attributes.get('Title').replace(' ', '_'),
        quantity=cube.attributes.get('Quantity').replace(' ', '_'),
        level=int(level.points[0]),
        timestamp=timestamp.units.num2date(
            timestamp.points[0]).strftime('%Y%m%d%H%M%S')
    )
    logger.info(title)
    ax.set_title(title)

    return fig, title


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate plots from directory of NAME data')
    parser.add_argument(
        'source_dir', help="Path to directory containing NAME files")
    parser.add_argument(
        'prefix', help="Filename prefix e.g. Air_Conc_grid_")
    parser.add_argument(
        '--output_dir',
        help="Path to directory to store plots (defaults to source_dir)",
        default=None)
    args = parser.parse_args()
    plot_name_files(Path(args.source_dir), args.prefix, Path(args.output_dir))
