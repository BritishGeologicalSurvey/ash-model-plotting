# Let's build a Dockerfile to run our tests for ash model plotting
# We use miniconda because the Iris package and its dependencies are 
# easiest to install from the conda-forge repository. 
FROM continuumio/miniconda3

# Install package dependencies
RUN apt-get update -y && \
    apt-get install -y \
     build-essential \
     curl \
     git 

# Install requirements
RUN conda install -y -c conda-forge iris \
    iris-sample-data flake8 pytest

# Install Python modules
ENV APP=/app
ENV PYTHONPATH=$APP
WORKDIR $APP
RUN mkdir ash-model-plotting

# Copy app files to container
COPY setup.py README.md .flake8 $APP/
COPY ash_model_plotting/ $APP/ash_model_plotting
COPY test/ $APP/test

# Clear old caches, if present
RUN find . -regextype posix-egrep -regex '.*/__pycache__.*' -delete
