"""
Plotting functions that draw and save figures from multi-dimensional cubes.
"""
import os
from pathlib import Path
import warnings

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from iris.exceptions import CoordinateNotFoundError
import iris.plot as iplt
from jinja2 import Template
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
import cf_units


def plot_4d_cube(cube, output_dir, file_ext='png', vaac_colours=False, **kwargs):
    """
    Plot multiple figures of 2D slices from a 4D cube in output directory.

    :param cube: Iris cube with 3 dimensions (time, lat, lon)
    :param output_dir: str; directory to save figure
    :param file_ext, file extension suffix for data format e.g. png, pdf
    :param kwargs: dict; extra arguments to pass to plt.savefig
    """
    metadata = {'created_by': 'plot_4d_cube',
                'attributes': cube.attributes,
                'plots': {}
                }

    base_output_dir = Path(output_dir)

    for tyx_slice in cube.slices(['time', 'latitude', 'longitude']):
        zlevel_str = _format_zlevel_string(tyx_slice)
        # Create new directory for each altitude level
        output_dir = base_output_dir / zlevel_str
        if not output_dir.is_dir():
            os.mkdir(output_dir)

        # Create placeholder for altitude level of nesting
        metadata['plots'][zlevel_str] = {}

        # Plot all the slices for that zlevel
        for yx_slice in tyx_slice.slices(['latitude', 'longitude']):
            timestamp = _format_timestamp_string(yx_slice)

            fig, title = draw_2d_cube(yx_slice, **kwargs)
            filename = output_dir / f"{title}.{file_ext}"
            fig.savefig(filename, **kwargs)
            plt.close(fig)

            metadata['plots'][zlevel_str][timestamp] = str(
                filename.relative_to(output_dir))

    return metadata


def plot_3d_cube(cube, output_dir, file_ext='png', vaac_colours=False, **kwargs):
    """
    Plot multiple figures of 2D slices from a cube in output directory.

    :param cube: Iris cube with 3 dimensions (time, lat, lon)
    :param output_dir: str; directory to save figure
    :param file_ext, file extension suffix for data format e.g. png, pdf
    :param kwargs: dict; extra args for draw_2d_cube and plt.savefig
    """
    metadata = {'created_by': 'plot_3d_cube',
                'attributes': cube.attributes,
                'plots': {}
                }

    output_dir = Path(output_dir)
    for i, timestamp in enumerate(cube.coord('time')):
        timestamp = _format_timestamp_string(cube[i, :, :])

        fig, title = draw_2d_cube(cube[i, :, :], vaac_colours=False, **kwargs)
        filename = output_dir / f"{title}.{file_ext}"
        fig.savefig(filename, **kwargs)
        plt.close(fig)

        metadata['plots'][timestamp] = str(filename.relative_to(output_dir))

    return metadata


def draw_2d_cube(cube, vmin=None, vmax=None, mask_less=1e-8,
                 vaac_colours=False, **kwargs):
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

    # Prepare colormap
    if vaac_colours and _vaac_compatible(cube):
        colors = ['#80ffff', '#939598']
        levels = [0.0002, 0.002, 0.004]
        cmap = matplotlib.colors.ListedColormap(colors)
        cmap.set_over('#e00404')
        norm = matplotlib.colors.BoundaryNorm(levels, cmap.N, clip=False)

    elif vaac_colours and not _vaac_compatible(cube):
        # Raise a warning but continue with default colour scheme
        warnings.warn("The VAAC colour scheme option (vaac_colours=True)"
                      " is only compatible with air concentration data."
                      " Falling back to use the default colour scheme...")
        cmap = "viridis"
        norm = None

    else:
        cmap = "viridis"
        norm = None

    # Plot data
    fig = plt.figure()
    mesh_plot = iplt.pcolormesh(cube, vmin=vmin, vmax=vmax,
                                cmap=cmap, norm=norm)
    ax = plt.gca()
    ax.coastlines(resolution='50m', color='grey')
    colorbar = fig.colorbar(mesh_plot, orientation='horizontal',
                            extend='max', extendfrac='auto')
    colorbar.set_label(f'{cube.units}')

    # Add tick marks
    ax.set_xlim(-35, 25)
    ax.set_ylim(35, 70)
    ax.set_xticks(ax.get_xticks(), crs=ccrs.PlateCarree())
    ax.set_yticks(ax.get_yticks(), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.grid(linewidth=0.5, color='grey', alpha=0.25, linestyle='--')

    # Get title attributes
    zlevel = _format_zlevel_string(cube)
    timestamp = _format_timestamp_string(cube)

    # Get and apply title, filter removes NoneType
    # elements before joining.
    title = '_'.join(filter(None, (
        cube.attributes.get('model_run_title').replace(' ', '_'),
        cube.attributes.get('quantity').replace(' ', '_'),
        str(zlevel),
        str(timestamp))))
    ax.set_title(title)

    return fig, title


def render_html(source, metadata):
    """
    Return string for HTML page displaying metadata and plots.

    :param source: str, source data for cube
    :param metadata: dict, metadata returned by plotting function
    :return: str, HTML for plot viewing page
    """
    # Prepare parameters
    title = ' - '.join(filter(None, (
        metadata['attributes'].get('model_run_title'),
        metadata['attributes'].get('quantity'),
        metadata['attributes'].get('Run time')
    )))
    params = dict(source=source, metadata=metadata, title=title)

    # Load template
    with open('ash_model_plotting/templates/ash_model_results.html') as f:
        template = Template(f.read())

    return template.render(**params)


def _format_timestamp_string(cube):
    """
    Return string representation of the timestamp for the cube. Method takes
    the first value in the time dimension e.g. assumes cube represents single
    time step.

    :param cube: Iris cube
    :return: str representation of timestamp
    """
    try:
        timestamp = cube.coord('time').points[0]
        timestamp = cube.coord('time').units.num2date(
            timestamp).strftime('%Y%m%d%H%M%S')
    except CoordinateNotFoundError:
        # No time coordinate on cube
        timestamp = ''

    return timestamp


def _get_zlevel_name(cube):
    """
    Return name of coordinate representing zlevel for cube.
    """
    known_z = set(['alt', 'altitude', 'flight_level'])
    cube_coords = [c.name() for c in cube.coords()]
    return known_z.intersection(cube_coords).pop()


def _format_zlevel_string(cube):
    """
    Return string representation of the zlevel for the cube. Method takes
    the first value in the zlevel dimension e.g. assumes cube represents
    single zlevel step.

    :param cube: Iris cube
    :return: str representation of zlevel
    """
    coord_types = {c.name() for c in cube.coords()}

    if 'altitude' in coord_types:
        zlevel = cube.coord('altitude').points[0]
        zlevel = f"{zlevel:05.0f}"
    elif 'alt' in coord_types:
        zlevel = cube.coord('alt').points[0]
        zlevel = f"{zlevel:05.0f}"
    elif 'Top height of each layer' in coord_types:
        zlevel = cube.coord('Top height of each layer').points[0]
        zlevel = f"{zlevel:05.0f}"
    elif 'flight_level' in coord_types:
        zlevel = cube.coord('flight_level').points[0]
        zlevel = f"FL{zlevel:03.0f}"
    else:
        # TODO: think about raising an exception here instead
        zlevel = ''

    return zlevel


def _get_zlevels(cube):
    """
    Return level values for z-coordinate of cube, typically alititude or
    flight level.

    :param cube: Iris cube
    :return list: z level numbers
    """
    if len(cube.coords()) != 4:
        raise ValueError("Cube does not have 4 dimensions")

    coord_types = {c.name() for c in cube.coords()}
    if 'altitude' in coord_types:
        return cube.coord('altitude').points.tolist()
    elif 'alt' in coord_types:
        return cube.coord('alt').points.tolist()
    elif 'Top height of each level' in coord_types:
        return cube.coord('Top height of each level').points.tolist()
    elif 'flight_level' in coord_types:
        return cube.coord('flight_level').points.tolist()
    else:
        raise ValueError("Cube doesn't have altitude or flight_level")


def _vaac_compatible(cube):
    """
    Check if the cube attempting to plot has compatible units
    (i.e. scientifically sensible), to use the official VAAC
    colour scheme.

    return boolean
    """
    return cube.units in (cf_units.Unit('g/m3'), cf_units.Unit('gr/m3'))
