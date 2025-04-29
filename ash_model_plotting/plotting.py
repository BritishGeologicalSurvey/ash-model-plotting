"""
Plotting functions that draw and save figures from multi-dimensional cubes.
"""
import os
from pathlib import Path
import logging
import warnings

from itertools import repeat
from multiprocessing import Manager, get_context

# Import matplotlib before Iris to allow backend setting
import matplotlib

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from iris.exceptions import CoordinateNotFoundError
from jinja2 import Template
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
import cf_units

# Configure matplotlib
matplotlib.use('agg')
mpl_logger = logging.getLogger("matplotlib")
mpl_logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
POOL_LOGGER_LEVEL = logging.INFO


def plot_4d_cube(cube, output_dir, file_ext='png', **kwargs):
    """
    Plot multiple figures of 2D slices from a 4D cube in output directory.

    :param cube: Iris cube with 3 dimensions (time, lat, lon)
    :param output_dir: str; directory to save figure
    :param file_ext, file extension suffix for data format e.g. png, pdf
    :param kwargs: dict; extra arguments to pass to plot_2d_cube and
        plt.savefig e.g. limits, vaac_colours, dpi, bbox_inches
    """
    metadata = {'created_by': 'plot_4d_cube',
                'attributes': dict(cube.attributes),
                'plots': {}
                }

    base_output_dir = Path(output_dir)
    vaac_colours = kwargs.get('vaac_colours', False)
    limits = kwargs.get('limits', None)
    clon = kwargs.get('clon', 0)
    serial = kwargs.get('serial', False)

    for tyx_slice in cube.slices_over(_get_zlevel_name(cube)):
        # Create new directory for each altitude level
        zlevel_str = _format_zlevel_string(tyx_slice)
        output_dir = base_output_dir / zlevel_str
        if not output_dir.is_dir():
            os.mkdir(output_dir)

        # Create a dictionary that can be shared between processes
        manager = Manager()
        fig_paths = manager.dict()

        # Create a list of arguments for plotting
        args = zip(tyx_slice.slices(['latitude', 'longitude']),
                   repeat(fig_paths), repeat(output_dir), repeat(file_ext),
                   repeat(limits), repeat(vaac_colours), repeat(clon), repeat(kwargs))

        if serial:
            for arg in args:
                # print(f'_save_yx_slice_figure: {arg}')
                _save_yx_slice_figure(*arg)
        else:
            #  Plot slices in parallel
            processes = len(os.sched_getaffinity(0))
            logger.debug('plot_4d for %s with %s processes', zlevel_str, processes)
            with get_context('spawn').Pool(
                    initializer=setup_pool_logger, initargs=(POOL_LOGGER_LEVEL,)
                    ) as pool:
                # 'spawn' is required to ensure each task gets fresh interpreter and
                # avoid issues with hanging caused by items shared across threads
                # starmap takes an iterable of iterables with the arguments
                pool.starmap(_save_yx_slice_figure, args)

        # Update metadata
        fig_paths = {key: fig_paths[key] for key in sorted(fig_paths.keys())}
        metadata['plots'][zlevel_str] = fig_paths

    return metadata


def setup_pool_logger(level):
    """
    Setup logger for use within multiprocessing pool
    """
    handler = logging.StreamHandler()
    formatter = logging.Formatter('pool process: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)


def plot_3d_cube(cube, output_dir, file_ext='png', **kwargs):
    """
    Plot multiple figures of 2D slices from a cube in output directory.

    :param cube: Iris cube with 3 dimensions (time, lat, lon)
    :param output_dir: str; directory to save figure
    :param file_ext, file extension suffix for data format e.g. png, pdf
    :param kwargs: dict; extra args for plot_2d_cube and plt.savefig
        e.g. limits, vaac_colours, dpi, bbox_inches
    """
    vaac_colours = kwargs.get('vaac_colours', False)
    limits = kwargs.get('limits', None)
    clon = kwargs.get('clon', 0)
    serial = kwargs.get('serial', False)

    output_dir = Path(output_dir)

    # Create a dictionary that can be shared between processes
    manager = Manager()
    fig_paths = manager.dict()

    # Create a list of arguments for plotting
    # Slices of longitude, latitude represent different times
    args = zip(cube.slices(['latitude', 'longitude']),
               repeat(fig_paths), repeat(output_dir), repeat(file_ext),
               repeat(limits), repeat(vaac_colours), repeat(clon), repeat(kwargs))

    if serial:
        for arg in args:
            _save_yx_slice_figure(*arg)
    else:
        #  Plot slices in parallel
        processes = len(os.sched_getaffinity(0))
        logger.debug('plot_3d with %s processes', processes)
        with get_context('spawn').Pool(
                initializer=setup_pool_logger, initargs=(POOL_LOGGER_LEVEL,)
                ) as pool:
            # 'spawn' is required to ensure each task gets fresh interpreter and
            # avoid issues with hanging caused by items shared across threads
            # starmap takes an iterable of iterables with the arguments
            pool.starmap(_save_yx_slice_figure, args)

    # Create metadata, including sorted list of fig_paths
    fig_paths = {key: fig_paths[key] for key in sorted(fig_paths.keys())}
    metadata = {'created_by': 'plot_3d_cube',
                'attributes': dict(cube.attributes),
                'plots': fig_paths
                }

    return metadata


def savefig_safe(fig, filename, **kwargs):
    valid_args = {'dpi', 'facecolor', 'edgecolor', 'orientation', 'format',
                  'transparent', 'bbox_inches', 'pad_inches', 'metadata',
                  'pil_kwargs', 'backend'}

    # Filter kwargs to keep only valid arguments for savefig
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_args}

    fig.savefig(filename, **filtered_kwargs)


def _save_yx_slice_figure(yx_slice, fig_paths, output_dir, file_ext, limits,
                          vaac_colours, clon, kwargs):
    """
    Call plot_2d_cube and save result in output_dir with name based on slice
    metadata.  This function is used by plot_3d_cube and plot_4d_cube functions
    and intended for use within multiprocessing.

    The fig_paths Manager dictionary is updated independently be each running
    process.

    :param yx_slice: 2d Iris cube (slice of larger cube)
    :param fig_paths: dict; filenames for figures for each timestamp
    :param output_dir: str; directory to save figure
    :param file_ext, file extension suffix for data format e.g. png, pdf
    :param kwargs: dict; extra args for plot_2d_cube and plt.savefig
        e.g. limits, vaac_colours, dpi, bbox_inches
    """
    timestamp = _format_timestamp_string(yx_slice)

    fig, title = plot_2d_cube(yx_slice, vaac_colours=vaac_colours,
                              limits=limits, clon=clon)
    filename = output_dir / f"{title}.{file_ext}"

    savefig_safe(fig, filename, **kwargs)
    plt.close(fig)
    logger.debug("Plotted %s on process %s", title, os.getpid())

    # Update shared dictionary of timestamps
    fig_paths[timestamp] = str(filename.relative_to(output_dir))


def plot_2d_cube(cube, vmin=None, vmax=None, mask_less=1e-8,
                 vaac_colours=False, limits=None, clon=0):
    """
    Draw a map of a two dimensional cube.  Cube should have two spatial
    dimensions (e.g. latitude, longitude).  All other dimensions (time,
    altitude) should be scalar dimensions.

    The figure and title are returned to allow user to save if required.

    :param cube: iris Cube
    :param vmin: Optional minimum value for scale
    :param vmax: Optional maximum value for scale
    :param mask_less: float, values beneath this are masked out
    :param vaac_colours: bool, use cyan, grey, red aviation zones
    :param limits: tuple (xmin, ymin, xmax, ymax), bounding box for plot
    :return fig: handle to Matplotlib figure
    :return title: str; title of plot generated from cube attributes
    """
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
    ax = plt.axes(projection=ccrs.PlateCarree(clon))
    mesh_plot = ax.pcolormesh(cube.coord('longitude').points, cube.coord('latitude').points,
                              cube.data, transform=ccrs.PlateCarree(),
                              vmin=vmin, vmax=vmax, cmap=cmap, norm=norm)

    ax.coastlines(resolution='50m', color='grey')
    colorbar = fig.colorbar(mesh_plot, orientation='horizontal',
                            extend='max', extendfrac='auto')
    colorbar.set_label(f'{cube.units}')

    # Set axis limits
    if limits:
        xmin, ymin, xmax, ymax = limits
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

    # # cant make gridlines work with crossing the dateline!
    xticks = ax.get_xticks()
    # print(f'xticks: {xticks}')
    _ = ax.set_xticks(xticks, crs=ccrs.PlateCarree(clon))

    # x2 = (xticks + 180)
    # x2[x2>180] += -360
    # print(f'x2: {x2}')
    # _ = ax.set_xticklabels(x2)

    yticks = ax.get_yticks()
    # print(f'yticks: {yticks}')
    yticks[0] = max(yticks[0], -90)
    yticks[-1] = min(yticks[-1], 90)
    # print(f'yticks: {yticks}')
    _ = ax.set_yticks(yticks, crs=ccrs.PlateCarree(clon))

    lon_formatter = LongitudeFormatter()
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    ax.grid()

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
    here = Path(__file__).parent
    template_file = here / 'templates' / 'ash_model_results.html'
    with open(template_file) as f:
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
    known_z = set(['alt', 'altitude', 'flight_level', 'z coordinate of x-y plane cuts',
                   'Top height of each layer'])
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
    elif 'z coordinate of x-y plane cuts' in coord_types:
        zlevel = cube.coord('z coordinate of x-y plane cuts').points[0]
        zlevel = f"{zlevel:05.0f}"
    elif 'flight_level' in coord_types:
        lower, upper = cube.coord('flight_level').bounds[0]
        zlevel = f"FL{lower:03.0f}-{upper:03.0f}"
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
    elif 'Top height of each layer' in coord_types:
        return cube.coord('Top height of each layer').points.tolist()
    elif 'flight_level' in coord_types:
        return cube.coord('flight_level').points.tolist()
    elif 'z coordinate of x-y plane cuts' in coord_types:
        return cube.coord('z coordinate of x-y plane cuts').points.tolist()
    else:
        raise ValueError("Cube doesn't have altitude or flight_level")


def _vaac_compatible(cube):
    """
    Check if the cube attempting to plot has compatible units
    (i.e. scientifically sensible), to use the official VAAC
    colour scheme.

    return boolean
    """
    # Note: Technically "gr/m3" represents "grains per cubic metre,
    # we include this check because an older version of Fall 3D
    # uses this abbreviation for grams, rather than the standard "g".
    # This convention is based on the udunits package conventions.
    return cube.units in (cf_units.Unit('g/m3'), cf_units.Unit('gr/m3'))
