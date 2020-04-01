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

This installation method makes scripts available on the `$PATH` of the virtual
environment, so they can be called from anywhere e.g. `plot_ash_model_results`.

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
fall3d_result = Fall3DAshModelResult('test/data/fall3d_operational.nc')
hysplit_result = HysplitAshModelResult('test/data/hysplit_operational.nc')

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


### Custom variable names

The names of the variables where the `ash-model-plotting` finds data are
stored in the following class variables:

+ `_air_concentration_names`
+ `_total_column_names`
+ `_total_deposition_names`

These are *set* variables that can be extended in the source code.
Alternatively, custom sub-classes can be created and the values overridden,
e.g.

```python
from AshModelPlotting import Fall3DAshModelResult

class MyCustomFall3DAshModelResult(Fall3DAshModelResult):
    _air_concentration_names = {'CON'}
    _total_column_names = {'COL_MASS'}
    _total_deposition_names = {'LOAD'}
    _zlevel_names = {'m (a. s. l.)'}

result = MyCustomFall3DAshModelResult('path/to/result/file.nc')
```

Note that some result sets mix ground and airborne values in the same file.
For these, it may be necessary to specify the `_zlevel_names` to extract those
correctly.


### Plot all data

The `plot_ash_model_results.py` script was created to plot air_concentration,
total column mass and total deposition from a set of model results.
The inputs are filename, model type and output directory.

Get instructions for plotting script:

```bash
python ash_model_plotting/plot_ash_model_results.py --help
```

Plot set of ash model results:

```bash
python ash_model_plotting/plot_ash_model_results.py \
  test/data/VA_Tutorial_NAME_output.nc \
  --model_type name --output_dir ./
```

This will create a the plots in the current directory.
There are plots for air concentration, total column and total deposition.
Plots for air concentration within are stored in subdirectories for each level (altitude) in the data.
If the `output_dir` is not specified, plots are written to the data directory.
If the `output_dir` does not exist, it will be created.

If `ash-model-plotting` has been installed via `pip`, the script will be added
to the virtual environment $PATH.


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

