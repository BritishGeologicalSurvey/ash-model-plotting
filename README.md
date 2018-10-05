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

These (and others) can be installed as follows.


## Installation via Conda (recommended)

Download and run the Miniconda3 installer for Linux, Mac or Windows from the [Conda website](https://conda.io/miniconda.html).
Create an 'environment' and install Iris and other Python packages:

```
conda create -y -c conda-forge -n ash-model-plotting iris iris-sample-data ipython
```

Activate the virtual environment:

```
source activate ash-model-plotting
```

The virtual environment isolates the Python packages used by ash-model-plotting from the rest of the system.
This means that they will not interfere with each other.

Deactivate the virtual environment:

```
source deactivate
```

## Running via Docker

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

## Installation for development (on Ubuntu Linux)

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

