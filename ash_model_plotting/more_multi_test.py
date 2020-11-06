# coding: utf-8
import json
import logging
import os
import time

from pathlib import Path

from ash_model_plotting import NameAshModelResult
from ash_model_plotting.plotting import plot_3d_cube
from ash_model_plotting.plotting import logger as ampp_logger

logger = logging.getLogger(__name__)


def main():
    """do this"""
    directory = Path('/tmp') / 'multi'
    if not directory.is_dir():
        directory.mkdir()

    name_dir = Path('/home/jostev/dev/ash-model-plotting/ADM_outputs/NAME/')
    files = [str(p.absolute()) for p in name_dir.glob('TotCol*.txt')]
    result = NameAshModelResult(files)
    metadata = plot_3d_cube(result.total_column[:, :, :], directory)
    logger.debug(metadata)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    #ampp_logger.setLevel(logging.DEBUG)
    starttime = time.time()
    logger.debug("Starting run...")

    main()

    logger.debug("Run complete in %s seconds", time.time() - starttime)
