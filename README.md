# Ash Model Plotting

> Code to plot and compare the results from volcanic ash dispersion model runs.

The plotting scripts are based on the following Python libraries.

+ [Iris](https://scitools.org.uk/iris/docs/latest): "A powerful,
  format-agnostic, and community-driven Python library for analysing and
visualising Earth science data."
+ [Cartopy](https://scitools.org.uk/cartopy/docs/v0.16/index.html): "...a Python
  package designed for geospatial data processing in order to produce maps and other geospatial data analyses."
+ [Matplotlib](https://matplotlib.org/): "...a Python 2D plotting library which
  produces publication quality figures in a variety of hardcopy formats and
  interactive environments across platforms."

See below for [dependency installation instructions](#dependencies).
These must be installed and the correct Python environment configured before running scripts.


## Installation

### Prepare environment with dependencies

Anaconda Python is used because it provides an easy way to install all the
dependencies required by Iris.
Download and run the Miniconda3 installer for Linux, Mac or Windows from the [Conda website](https://conda.io/miniconda.html).
Create an 'environment' and install Iris and other Python packages:

```bash
conda create -y -c conda-forge -n ash-model-plotting \
  iris ipython numpy matplotlib
```

Activate the virtual environment:

```bash
conda activate ash-model-plotting
```

The virtual environment isolates the Python packages used by ash-model-plotting from the rest of the system.
This means that they will not interfere with each other.

You can deactivate the virtual environment with:

```bash
conda deactivate
```

### Install ash-model-plotting

Checkout the code from Git:

```
git clone git@bitbucket.org:jsteven5/ash-model-plotting.git
cd ash-model-plotting
```

The repository contains a `setup.py` file installed ash-model-plotting so it can be used within the virtual environment from anywhere on the system.
Install is as follows.

```bash
python -m pip install -e .
```

The `-e` flag means that changes made to files in this source directory will be
applied without having to reinstall the module.

This installation should make a number of scripts available on the `$PATH`,
such as `plot_ash_model_results`.

## How to use ash-model-plotting

`ash_model_plotting` provides a wrapper class around the Iris data cube.
This AshModelResult class has convenience functions for accessing data for air
concentration, total column loading and total deposition.
The data are returned as Iris cubes and can be further processed as required.
There are different AshModelResult classes for different dispersion model
result types.
There are also functions for plotting these results.

`ash-model-plotting` is most easily used in an interactive environment (e.g.
IPython terminal or Jupyter notebook).

```python
from glob import glob
from ash_model_plotting import (
    NameAshModelResult,
    Fall3DAshModelResult,
    HysplitAshModelResult
    )

# Load NAME data from text files, or Fall3D/Hysplit from NetCDF
name_files = glob('test/data/*.txt')
name_result = NameAshModelResult(name_files)
fall3d_result = Fall3DAshModelResult('test/data/fall3d_realistic_res_clip.nc')
hysplit_result = HysplitAshModelResult('test/data/hysplit_cdump.nc')

# Access subsets of data as class "properties"
print(name_result.air_concentration)
print(name_result.total_column)
print(name_result.total_deposition)

# Easily plot different attributes
fall3d_result.plot_air_concentration('path/to/output/directory')
fall3d_result.plot_total_column('path/to/output/directory')
fall3d_result.plot_total_deposition('path/to/output/directory')
```

This class uses the `plot_4d_cube`, `plot_3d_cube` and `draw_2d_cube` functions from `plotting.py` internally.

## Analysis scripts for earlier versions

The following examples were based on earlier version of ash-model-plotting.
They will be updated soon.

### Convert NAME to netCDF

The `name_to_netcdf.py` script will collect all the NAME output files in a directory and convert them into a single NetCDF file.

Get instructions for plotting script:

```bash
python ash_model_plotting/name_to_netcdf.py --help
```

Convert NAME data to NetCDF4 from the command line:

```bash
python ash_model_plotting/name_to_netcdf.py /path/to/ADM_outputs/NAME
```


### Plot all data

The plot_ash_model_results.py script was created to plot NAME data.

Get instructions for plotting script:

```bash
python ash_model_plotting/plot_ash_model_results.py --help
```

Plot NAME data (after converting to NetCDF4) from the command line:

```bash
python ash_model_plotting/plot_ash_model_results.py /path/to/ADM_outputs/NAME/VA_Tutorial_NAME_output.nc --output_dir ./
```

This will create a the plots in the current directory.
There are plots for air concentration, total column and total deposition.
Plots for air concentration within are stored in subdirectories for each level (altitude) in the data.
If the `output_dir` is not specified, plots are written to the data directory.
If the `output_dir` does not exist, it will be created.



### REFIR analysis

The following section contains information specific to a study using the REFIR
tool.

To analyse output from REFIR model runs, use the following command:

```bash
python ash_model_plotting/analyse_refir_outputs.py  /path/to/name_results --output_dir /path/to/outputs
```

The script extracts the maximum concentration and the area above the advisory
threshold for each of the modelled runs.
It creates a CSV file with a summary of the data and bar charts comparing the
different models.

Maps can be plotted for each model run with:

```bash
python ash_model_plotting/plot_ash_model_results /path/to/name_results/Fields_grid88*.txt --output_dir /path/to/outputs
```

