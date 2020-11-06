# coding: utf-8
import json
import logging
import os
import time

from pathlib import Path

from ash_model_plotting import Fall3DAshModelResult
from ash_model_plotting.plotting import plot_4d_cube
from ash_model_plotting.plotting import logger as ampp_logger

logger = logging.getLogger(__name__)


def main():
    """do this"""
    directory = Path('/tmp') / 'multi'
    if not directory.is_dir():
        directory.mkdir()

    result = Fall3DAshModelResult('/home/jostev/dev/ash-model-plotting/ADM_outputs/'
                                  'FALL3D/realistic.res.nc')
    metadata = plot_4d_cube(result.air_concentration[:5, :20, :, :], directory)
    logger.debug(metadata)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    ampp_logger.setLevel(logging.DEBUG)
    starttime = time.time()
    logger.debug("Starting run...")
    logger.debug("")

    main()

    logger.debug("")
    logger.debug("Run complete in %s seconds", time.time() - starttime)
