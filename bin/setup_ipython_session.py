"""Run this script in an IPython terminal with `%run bin/setup_ipython_session.py`
to quickstart a session with working imports already loaded."""
# coding: utf-8
# flake8: noqa

get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

import iris
from ash_model_plotting import NameAshModelResult, HysplitAshModelResult, Fall3DAshModelResult
from glob import glob

name = NameAshModelResult(glob('test/data/*.txt'))
fall3d = Fall3DAshModelResult('test/data/fall3d_realistic_res_clip.nc')
hysplit = HysplitAshModelResult('test/data/hysplit_cdump.nc')
