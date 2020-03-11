# Developer notes and contribution guide

## Running tests

There are unit and integration tests to check that the code does as is expected.  Run them with:

```
conda install -c conda-forge ipdb flake8 pytest pytest-icdiff
pytest -vs test
```

## Installation for development (on Ubuntu Linux)

This method explains how to install Iris with all dependencies on Ubuntu Linux.
I is only recommended if you intend to make changes to Iris itself.

### Install dependencies:

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

### Sort out pyke

Pyke is is needed to run `setup.py`
Download pyke3-1.1.1.zip from [http://pyke.sourceforge.net](https://pyke.sourceforge.net)

```
unzip pyke3-1.1.1.zip
pip install 2to3
cd pyke-1.1.1
./run_2to3
python setup.py install
```

### Install Iris

```
cd ../iris
pip install -e .
```
