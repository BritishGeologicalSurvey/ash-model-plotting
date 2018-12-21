"""
Plotting functions that draw and save figures from multi-dimensional cubes.
"""
from iris.exceptions import CoordinateNotFoundError
import iris.plot as iplt
import matplotlib.pyplot as plt

# TODO:
# plot_2d_series, plot_3d_series
# loop over altitude then loop over time


def draw_2d_cube(cube, vmin=None, vmax=None):
    """
    Draw a map of a two dimensional cube.  Cube should have two spatial
    dimensions (e.g. latitude, longitude).  All other dimensions (time,
    altitude) should be scalar dimensions.

    The figure and title are returned to allow user to save if required.

    :param cube: iris Cube
    :param vmin: Optional minimum value for scale
    :param vmax: Optional maximum value for scale
    :return fig: handle to Matplotlib figure
    :return title: str; title of plot generated from cube attributes
    """
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
        altitude = f"{altitude:05.0f}_"  # Add underscore for use in composite title
    except CoordinateNotFoundError:
        # No altitude coordinate on cube
        altitude = ''

    try:
        timestamp = cube.coord('time').points[0]
        timestamp = cube.coord('time').units.num2date(timestamp).strftime('%Y%m%d%H%M%S')
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
