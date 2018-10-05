# coding: utf-8
import logging

import iris
import iris.plot as iplt
import matplotlib.pyplot as plt

# Monkey patch GeoAxes to fix Matplotlib v3.0.0 - related bug
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
GeoAxes._pcolormesh_patched = Axes.pcolormesh

logging.basicConfig(level=logging.INFO)

cubes = iris.load('Air_Conc_grid_201004170000.txt')
cube = cubes[1]
levels = cube.coord('altitude')
timestamp = cube.coord('time')

for i, level in enumerate(levels):
    iplt.pcolormesh(cube[i, :, :])
    plt.gca().coastlines()
    name = "{title}_{quantity}_{level:05d}_{timestamp}.png".format(
        title=cube.attributes.get('Title').replace(' ', '_'),
        quantity=cube.attributes.get('Quantity').replace(' ', '_'),
        level=int(level.points[0]),
        timestamp=timestamp.units.num2date(timestamp.points[0]).strftime('%Y%m%d%H%M%S')
    )
    logging.info(name)
    plt.title(name)
    plt.savefig(name)
    plt.close()


