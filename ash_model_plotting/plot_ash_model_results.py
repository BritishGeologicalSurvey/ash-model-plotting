# coding: utf-8
import argparse
import logging
import os
from pathlib import Path

from ash_model_plotting.ash_model_result import (
    AshModelResult,
    AshModelResultError,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def plot_name_files(input_file, output_dir=None):
    """
    Plot ash model results the layers in the input_file.  Plots are made
    for air_concentration, total_column and total_deposition for each
    timestamp and altitude.

    :param input_file: str, path to source file (netCDF4)
    :param output_dir: str, directory for plot output (will be created if does
        not exist.
    """
    # Prepare output directory
    if not output_dir:
        output_dir = Path(input_file).parent
    else:
        output_dir = Path(output_dir)

    if not output_dir.exists():
        os.mkdir(output_dir)

    # Load data
    result = AshModelResult(input_file)

    # Make plots
    logger.info(f'Writing plots from {input_file} to {output_dir}')
    for attribute in ('air_concentration', 'total_column', 'total_deposition'):
        try:
            logger.info(f'Plotting {attribute}')
            getattr(result, f'plot_{attribute}')(output_dir,
                                                 bbox_inches='tight')
        except AshModelResultError:
            logger.info(f'No {attribute} data found')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate plots from netCDF4 file of NAME data')
    parser.add_argument(
        'input_file', help="Input netCDF4 file path")
    parser.add_argument(
        '--output_dir',
        help=("Path to directory to store plots (defaults to source_dir), "
              "creates directory if doesn't exist"),
        default=None)
    args = parser.parse_args()
    plot_name_files(args.input_file, args.output_dir)
