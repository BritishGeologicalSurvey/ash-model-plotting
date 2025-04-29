# Let's build a Dockerfile to run our tests for ash model plotting
# We use miniconda because the Iris package and its dependencies are 
# easiest to install from the conda-forge repository. 
FROM continuumio/miniconda3:25.1.1-1

# Setup working directory
WORKDIR /test

# Install requirements
COPY environment_docker.yml .
RUN conda env create -f environment_docker.yml

# Copy app files to container
COPY .flake8 .
COPY ash_model_plotting/ ./ash_model_plotting
COPY test/ ./test

# Clear old caches, if present
RUN find . -regextype posix-egrep -regex '.*/__pycache__.*' -delete

# Allow tests to be run with `docker run ash-model-plotting pytest test`
ENV PYTHONPATH=.
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ash-model-plotting", "/bin/bash", "-c"]
