"""
Script to plot NAME output files
"""
# coding: utf-8
import argparse
import logging
import os
from pathlib import Path

from ash_model_plotting import (
    NameAshModelResult,
    Fall3DAshModelResult,
    HysplitAshModelResult,
    AshModelResultError,
)

logger = logging.getLogger('plot_ash_model_results')


MODEL_TYPES = {
    'name': NameAshModelResult,
    'fall3d': Fall3DAshModelResult,
    'hysplit': HysplitAshModelResult
}


def plot_results(results, model_type, limits, vaac_colours, output_dir):
    """
    Plot ash model results the layers in the input_files.  Plots are made
    for air_concentration, total_column and total_deposition for each
    timestamp and altitude.

    :param input_files: list of str, paths to source file (netCDF4)
    :param model_type: str, type of ash model result
    :param limits: list of float, xmin ymin xmax ymax for plot limits
    :param vaac_colours: bool, use VAAC colours (cyan, grey, red) for air
        concentration.
    :param output_dir: str, directory for plot output (will be created if does
        not exist.
    """
    # Prepare output directory
    if not output_dir:
        first_file = results[0]
        output_dir = Path(first_file).parent
    else:
        output_dir = Path(output_dir)

    if not output_dir.exists():
        os.mkdir(output_dir)

    # Load data
    # Extract filename as string if only one provided
    if len(results) == 1:
        results = results[0]
    result = MODEL_TYPES[model_type](results)

    # Make plots
    logger.info(f'Writing plots from {results} to {output_dir}')
    for attribute in ('air_concentration', 'total_column', 'total_deposition'):
        try:
            logger.info(f'Plotting {attribute}')
            getattr(result, f'plot_{attribute}')(output_dir,
                                                 limits=limits,
                                                 vaac_colours=vaac_colours,
                                                 bbox_inches='tight')
        except AshModelResultError:
            logger.info(f'No {attribute} data found')


def main():
    """Parse arguments and call plot_name_files."""
    parser = argparse.ArgumentParser(
        description='Generate plots from NAME data .txt files')
    parser.add_argument(
        'results',
        help="Result file path(s)",
        nargs='+')
    parser.add_argument(
        '--model_type',
        help="Type of model",
        choices=MODEL_TYPES.keys(),
        default='name', type=str)
    parser.add_argument(
        '--limits',
        help="Plot axes limits: xmin ymin xmax ymax",
        default=None, type=float,
        nargs=4)
    parser.add_argument(
        '--vaac_colours',
        help="Use VAAC colours (cyan, grey, red) for air concentration",
        action='store_true')
    parser.add_argument(
        '--output_dir',
        help=("Path to directory to store plots (defaults to source_dir), "
              "creates directory if doesn't exist"),
        default=None)
    parser.add_argument(
        '--verbose',
        help=("Print debugging messages in output"),
        action='store_true')
    args = parser.parse_args()

    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.getLogger().setLevel(log_level)

    plot_results(args.results, args.model_type, args.limits,
                 args.vaac_colours, args.output_dir)


if __name__ == '__main__':
    # Suppress warning messages from Matplotlib etc
    os.environ['PYTHONWARNINGS'] = 'ignore'

    # Configure logger
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)

    # Run script
    main()
