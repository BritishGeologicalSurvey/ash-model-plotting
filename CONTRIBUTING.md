# Developer notes and contribution guide

## Local development environment

### Environment setup

First create and activate a conda virtual environment as specified in the [README.md](README.md)
Then checkout the code from Git:

```
git clone git@github.com:BritishGeologicalSurvey/ash-model-plotting.git
cd ash-model-plotting
```

Install the `ash-model-plotting` library to the current virtual environment:

```bash
python -m pip install -e .
```

The `-e` flag means that changes made to files in this source directory will be
applied without having to reinstall the module.

This installation method makes scripts available on the `$PATH` of the virtual
environment, so they can be called from anywhere e.g. `plot_ash_model_results`.

### Running tests

There are unit and integration tests to check that the code does as is expected.
Run them with:

```bash
pytest -vs test
```

### Docker-based testing

The repository includes a Dockerfile to allow the tests to be run in a constrained environment.
Build the docker container with:

```bash
docker build -t ash-model-plotting .
```

Run the tests with:

```bash
docker run --rm ash-model-plotting flake8 ash_model_plotting
docker run --rm ash-model-plotting pytest test
```
