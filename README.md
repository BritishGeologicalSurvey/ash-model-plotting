# Ash Model Plotting

> Code to plot and compare the results from volcanic ash dispersion model runs.

## Software

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


## Setup

Checkout the code from Git:

```
git clone git@bitbucket.org:jsteven5/ash-model-plotting.git
cd ash-model-plotting
```

### Installation via Conda (recommended)

Download and run the Miniconda3 installer for Linux, Mac or Windows from the [Conda website](https://conda.io/miniconda.html).
Create an 'environment' and install Iris and other Python packages:

```
conda create -y -c conda-forge -n ash_model_plotting iris iris-sample-data ipython numpy matplotlib
```

Activate the virtual environment:

```
source activate ash_model_plotting
```

The virtual environment isolates the Python packages used by ash_model_plotting from the rest of the system.
This means that they will not interfere with each other.

Deactivate the virtual environment:

```
source deactivate
```

To be able to import from the `ash_model_plotting` repository, it may be
necessary to add it to the Python path:

```bash
export PYTHONPATH=.
```

### Environment-wide installation

The repository contains a `setup.py` file that can install the module and make
it available from anywhere on the system.
If you have access to `pip`, it can be installed as follows:

```bash
python -m pip install -e .
```

The `-e` flag means that changes made to files in this source directory will be
applied without having to reinstall the module.

This installation should make a number of scripts available on the `$PATH`,
such as `plot_ash_model_results`.


## REFIR analysis

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


# Previous information

The text below belongs to a previous incarnation of the script and is not
relevant to the current REFIR project.

## Convert NAME to netCDF

The `name_to_netcdf.py` script will collect all the NAME output files in a directory and convert them into a single NetCDF file.

Get instructions for plotting script:

```bash
python ash_model_plotting/name_to_netcdf.py --help
```

Convert NAME data to NetCDF4 from the command line:

```bash
python ash_model_plotting/name_to_netcdf.py /path/to/ADM_outputs/NAME
```


## Plot all data

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


## AshModelResult

`ash_model_plotting` provides a wrapper class around the Iris data cube.
It has convenience functions for accessing data of different types.
It is used as follows:

```python
from ash_model_plotting import AshModelResult
result = AshModelResult('path/to/VA_Tutorial_NAME_output.nc')

# Access subsets of data
print(result.air_concentration)
print(result.total_column)
print(result.total_deposition)

# Plot subsets of data
result.plot_air_concentration('path/to/output/directory')
result.plot_total_column('path/to/output/directory')
result.plot_total_deposition('path/to/output/directory')
```

This class uses the `plot_4d_cube`, `plot_3d_cube` and `draw_2d_cube` functions from `plotting.py` internally.


## For Developers

#### Running tests

There are unit and integration tests to check that the code does as is expected.  Run them with:

```
export PYTHONPATH=.
pytest -vs test
```

## Dependencies


Developers should also run:

```
conda install -c conda-forge ipdb flake8 pytest pytest-icdiff
```
