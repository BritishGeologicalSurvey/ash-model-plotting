"""
Plotting functions that draw and save figures from multi-dimensional cubes.
"""
import os
from pathlib import Path

from iris.exceptions import CoordinateNotFoundError
import iris.plot as iplt
import matplotlib.pyplot as plt
import numpy as np


def plot_4d_cube(cube, output_dir, file_ext='png', **kwargs):
    """
    Plot multiple figures of 2D slices from a 4D cube in output directory.

    :param cube: Iris cube with 3 dimensions (time, lat, lon)
    :param output_dir: str; directory to save figure
    :param file_ext, file extension suffix for data format e.g. png, pdf
    :param kwargs: dict; extra arguments to pass to plt.savefig
    """
    base_output_dir = Path(output_dir)
    for i, altitude in enumerate(cube.coord('altitude')):
        # Create new directory for each altitude level
        output_dir = base_output_dir / f'{int(altitude.points[0]):05d}'
        if not output_dir.is_dir():
            os.mkdir(output_dir)

        # Plot all the slices for that altitude
        for j, timestamp in enumerate(cube.coord('time')):
            fig, title = draw_2d_cube(cube[i, j, :, :], **kwargs)
            filename = output_dir / f"{title}.{file_ext}"
            fig.savefig(filename, **kwargs)
            plt.close(fig)


def plot_3d_cube(cube, output_dir, file_ext='png', **kwargs):
    """
    Plot multiple figures of 2D slices from a cube in output directory.

    :param cube: Iris cube with 3 dimensions (time, lat, lon)
    :param output_dir: str; directory to save figure
    :param file_ext, file extension suffix for data format e.g. png, pdf
    :param kwargs: dict; extra args for draw_2d_cube and plt.savefig
    """
    output_dir = Path(output_dir)
    for i, timestamp in enumerate(cube.coord('time')):
        fig, title = draw_2d_cube(cube[i, :, :], **kwargs)
        filename = output_dir / f"{title}.{file_ext}"
        fig.savefig(filename, **kwargs)
        plt.close(fig)


def draw_2d_cube(cube, vmin=None, vmax=None, mask_less=1e-8, **kwargs):
    """
    Draw a map of a two dimensional cube.  Cube should have two spatial
    dimensions (e.g. latitude, longitude).  All other dimensions (time,
    altitude) should be scalar dimensions.

    The figure and title are returned to allow user to save if required.

    :param cube: iris Cube
    :param vmin: Optional minimum value for scale
    :param vmax: Optional maximum value for scale
    :param mask_less: float, values beneath this are masked out
    :return fig: handle to Matplotlib figure
    :return title: str; title of plot generated from cube attributes
    """
    # Note **kwargs is used to catch extra arguments that may be passed
    # as a result of unpacking **kwargs into calling functions

    # Mask out data below threshold
    cube.data = np.ma.masked_less(cube.data, mask_less)

    # Plot data
    fig = plt.figure()
    mesh_plot = iplt.pcolormesh(cube, vmin=vmin, vmax=vmax)
    ax = plt.gca()
    ax.coastlines(resolution='50m', color='grey')
    colorbar = fig.colorbar(mesh_plot, orientation='horizontal')
    colorbar.set_label(f'{cube.long_name.title()} ({cube.units})')

    # Get title attributes
    try:
        altitude = cube.coord('altitude').points[0]
        # Add underscore for use in composite title
        altitude = f"{altitude:05.0f}_"
    except CoordinateNotFoundError:
        # No altitude coordinate on cube
        altitude = ''

    try:
        timestamp = cube.coord('time').points[0]
        timestamp = cube.coord('time').units.num2date(
            timestamp).strftime('%Y%m%d%H%M%S')
    except CoordinateNotFoundError:
        # No time coordinate on cube
        timestamp = ''

    # Get and apply title
    title = "{title}_{quantity}_{altitude}{timestamp}".format(
        title=cube.attributes.get('Title').replace(' ', '_'),
        quantity=cube.attributes.get('Quantity').replace(' ', '_'),
        altitude=altitude,
        timestamp=timestamp
    )
    ax.set_title(title)

    return fig, title
