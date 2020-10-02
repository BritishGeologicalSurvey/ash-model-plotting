"""
Messing around with multiprocessing
"""
import logging
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PLOT_COUNT = 5

logging.basicConfig(level=logging.DEBUG)


def plot_many():
    all_x = [range(x + 1) for x in range(PLOT_COUNT)]
    all_y = [range(y + 1) for y in range(PLOT_COUNT)]
    titles = [f'plot_{x}' for x in range(PLOT_COUNT)]
    directory = Path('/tmp') / 'multi'
    if not directory.is_dir():
        directory.mkdir()

    for i, title in enumerate(titles):
        plot_fig(all_x[i], all_y[i], title, directory)


def plot_fig(x, y, title, directory):
    logging.debug("Plotting %s", title)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(title)
    plt.savefig(Path(directory) / f"{title}.png")


if __name__ == '__main__':
    plot_many()
