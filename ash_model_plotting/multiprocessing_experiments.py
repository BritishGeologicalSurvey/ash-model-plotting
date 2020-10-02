"""
Messing around with multiprocessing
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_fig(x, y, title, directory):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title(title)
    plt.savefig(Path(directory) / f"{title}.png")


if __name__ == '__main__':
    x = range(5)
    y = range(5)
    plot_fig(x, y, 'one_plot', '/tmp')
