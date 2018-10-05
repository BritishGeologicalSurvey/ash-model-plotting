## Software

The plotting scripts are based on the following Python libraries.

+ [Iris](https://scitools.org.uk/iris/docs/latest): "A powerful,
  format-agnostic, and community-driven Python library for analysing and
visualising Earth science data."

## Installation (on Ubuntu Linux)

Install most dependencies.

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

Sort out pyke, which is needed to install
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

The installation requirements have been stored in a Pipfile, which may be
useful in future.
