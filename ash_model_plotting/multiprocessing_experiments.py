"""
Messing around with multiprocessing
"""
import logging

from pathlib import Path
from itertools import repeat
from multiprocessing import Pool
from random import random

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PLOT_COUNT = 5

logging.basicConfig(level=logging.DEBUG)


def plot_many():
    # Prepare inputs
    all_x = [[random() for x in range(PLOT_COUNT)] for x in range(PLOT_COUNT)]
    all_y = [[random() for y in range(PLOT_COUNT)] for x in range(PLOT_COUNT)]
    titles = [f'plot_{x}' for x in range(PLOT_COUNT)]
    directory = Path('/tmp') / 'multi'
    if not directory.is_dir():
        directory.mkdir()

    args = zip(all_x, all_y, titles, repeat(directory))
    with Pool() as pool:
        pool.starmap(plot_fig, args)


def plot_fig(x, y, title, directory):
    logging.debug("Plotting %s", title)
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_title(title)
    plt.savefig(Path(directory) / f"{title}.png")


if __name__ == '__main__':
    plot_many()
