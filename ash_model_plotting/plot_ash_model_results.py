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


def plot_name_files(input_files, output_dir=None):
    """
    Plot ash model results the layers in the input_files.  Plots are made
    for air_concentration, total_column and total_deposition for each
    timestamp and altitude.

    :param input_files: list of str, paths to source file (netCDF4)
    :param output_dir: str, directory for plot output (will be created if does
        not exist.
    """
    # Prepare output directory
    if not output_dir:
        first_file = input_files[0]
        output_dir = Path(first_file).parent
    else:
        output_dir = Path(output_dir)

    if not output_dir.exists():
        os.mkdir(output_dir)

    # Load data
    result = AshModelResult(input_files)

    # Make plots
    logger.info(f'Writing plots from {input_files} to {output_dir}')
    for attribute in ('air_concentration', 'total_column', 'total_deposition'):
        try:
            logger.info(f'Plotting {attribute}')
            getattr(result, f'plot_{attribute}')(output_dir,
                                                 bbox_inches='tight')
        except AshModelResultError:
            logger.info(f'No {attribute} data found')


def main():
    """Parse arguments and call plot_name_files."""
    parser = argparse.ArgumentParser(
        description='Generate plots from netCDF4 file of NAME data')
    parser.add_argument(
        'input_files',
        help="Input file path(s)",
        nargs='+')
    parser.add_argument(
        '--output_dir',
        help=("Path to directory to store plots (defaults to source_dir), "
              "creates directory if doesn't exist"),
        default=None)
    args = parser.parse_args()
    plot_name_files(args.input_files, args.output_dir)


if __name__ == '__main__':
    main()
