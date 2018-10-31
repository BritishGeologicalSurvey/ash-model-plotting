# coding: utf-8
import argparse
import glob
import logging
import os

import iris
import iris.plot as iplt
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

# Monkey patch GeoAxes to fix Matplotlib v3.0.0 - related bug
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
GeoAxes._pcolormesh_patched = Axes.pcolormesh

logging.basicConfig(level=logging.INFO)


def plot_name_files(source_dir, prefix, output_dir):
    """
    Read the files named 'source_dir/prefix*' and generate plots. Files are
    saved with `plots` dir.
    :param source_dir: str, path to directory containing files
    :param prefix: str, common prefix of files to parse
    """
    if not output_dir:
        output_dir = source_dir
    logging.info(f'Writing files to {output_dir}')

    for source_file in glob.glob(os.path.join(source_dir, prefix) + '*'):
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
    :param level: int, level value
    :param idx: int, index for given level
    :return fig, name: Matplotlib figure with plot and str with name
    """
    # Plot data
    fig = plt.figure()
    mesh_plot = iplt.pcolormesh(cube[idx, :, :])
    ax = plt.gca()
    ax.coastlines(resolution='50m')
    ax.grid(True)
    fig.colorbar(mesh_plot, orientation='horizontal')

    # Get and set title
    timestamp = cube.coord('time')
    title = "{title}_{quantity}_{level:05d}_{timestamp}.png".format(
        title=cube.attributes.get('Title').replace(' ', '_'),
        quantity=cube.attributes.get('Quantity').replace(' ', '_'),
        level=int(level.points[0]),
        timestamp=timestamp.units.num2date(timestamp.points[0]).strftime('%Y%m%d%H%M%S')
    )
    logging.info(title)
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
        '--output_dir', help="Path to directory to store plots", default=None)
    args = parser.parse_args()
    plot_name_files(args.source_dir, args.prefix, args.output_dir)
