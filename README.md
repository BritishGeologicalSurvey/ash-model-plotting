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
git checkout git@kwvmxgit.ad.nerc.ac.uk:volcanology/ash_model_plotting.git
cd ash_model_plotting
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

### Running via Docker

An alternative to a local installation is to run a Jupyter Labs session with all the Iris dependencies installed.
This is good for interactive experimentation.
A Dockerfile is included to create the container.

```
docker build -t iris .
```

Jupyter Labs can be started via:

```
docker run -p 8888:8888 -v $(pwd):/home/iris --rm --name iris iris:latest
```

This will start a server that can see the files in the current directory.
The server can be run in the background by passing the `-d` flag.
The URL and token to access the webpage are then obtained via:

```
docker exec iris jupyter notebook list
```

### Installation for development (on Ubuntu Linux)

This method is only recommended if you intend to make changes to Iris itself.

First install dependencies:

```
pipenv --python 3.6
pipenv shell
git clone https://github.com/SciTools/iris
cd iris/requirements

# Install extra dependencies
sudo apt install libgeos-dev libproj-dev libudunits2-dev libgdal-dev python3-tk

# Install gdal with compiling set up
pip install Cython
pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==$(gdal-config --version)

# Install from files
pip install -r core.txt
pip install -r extensions.txt
pip install -r setup.txt
```

Download sample data

```
cd ../..
wget https://github.com/SciTools/iris-sample-data/archive/master.zip
```

Sort out pyke, which is needed to run `setup.py`
Download pyke3-1.1.1.zip from [https://pyke.sourceforge.net](https://pyke.sourceforge.net)
```
unzip pyke3-1.1.1.zip
pip install 2to3
cd pyke-1.1.1
./run_2to3
python setup.py install
```

Install IRIS
```
cd ../iris
pip install -e .
```

Install example data
```
cd ../iris/iris-sample-data-master
python setup.py install
```

