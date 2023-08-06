# openqlab

[![pipeline status](https://gitlab.com/las-nq/openqlab/badges/master/pipeline.svg)](https://gitlab.com/las-nq/openqlab/commits/master)
[![coverage report](https://gitlab.com/las-nq/openqlab/badges/master/coverage.svg)](https://gitlab.com/las-nq/openqlab/commits/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


`openqlab` provides a collection of useful tools and helpers for the
analysis of lab data in the Nonlinear Quantum Optics Group at the University
of Hamburg.

Part of the content in this package was written during the PhD theses of
Sebastian Steinlechner and Tobias Gehring. It is currently maintained by
Sebastian Steinlechner, Christian Darsow-Fromm, Jan Petermann and is looking for more
volunteers who would like to contribute.

Read the latest changes in our [changelog](CHANGELOG.md).

## Documentation

* Current documentation of the [latest release](https://las-nq-serv.physnet.uni-hamburg.de/python/openqlab)
* Current documentation of the [latest development version](https://las-nq-serv.physnet.uni-hamburg.de/python/openqlab-stage)

## Features

* Importers for various file formats:
  * Agilent/Keysight scopes (binary and CSV)
  * Rohde & Schwarz spectrum analyzers
  * Tektronix spectrum analyzer
  * plain ascii
  * and a few more...
* easily create standard plots from measurement data
* design control loops
* analyze beam profiler data
* generate covariance matrices for N partite systems
* several postprocessing functions for entanglement data
* analyse and automatically plot squeezing data
* tools for working with dB units

## Installation

For a detailed installation instruction see the main [documentation](https://las-nq-serv.physnet.uni-hamburg.de/python/openqlab/).

## Usage

You will need an up-to-date Python 3 environment to use this package, e.g.
the Anaconda Python distribution will work just fine. Please refer to the
`requirements.txt` for a list of prerequisites (although these should be
installed automatically, if necessary).

For examples and details on how to use this package, please refer to the
documentation.

## Development

### Poetry
Use [Poetry](https://python-poetry.org/) to manage the development packages.
If you are missing a small how-to, just ask and write it. :)

```bash
poetry install
```

### Tests
Please write unittests if you add new features.
The structure for the test should represent the structure of the package itself.
Each subpackage should have its own folder prefixed with `test_` and should contain subfolders with the same structure.
Every `.py` file (module) should be represented by one folder containing test files that test specific functions of that file.
For example:
- `tests`
    - `test_subpackage1`
        - `test_module1`
            - `test_function1_of_module1.py`
            - `test_function2_of_module1.py`
        - `test_module2`
            - `test_function1_of_module2.py`
            - `test_function2_of_module2.py`
    - `test_subpackage2`

For very simple classes or modules, the whole module can be tested in one `test_module.py` file but may still be contained inside a folder with the same name.
All tests located in `src/test/*` are automatically tested when pushing to Gitlab.

To run them manually use:
```bash
make test
```

### Code Formatter

We use [`pre-commit`](https://pre-commit.com/#python) for automatic code formatting before committing.
It is automatically installed with the development packages.
The command to enable the hooks is:
```bash
pre-commit install
```

### Changelog

Please write every change that seems significant in the [CHANGELOG.md](CHANGELOG.md) file.

### Release a new version

#### 1. Use poetry to change the version number
```bash
poetry version patch  # small fixes
poetry version minor  # small features
poetry version major  # breaking changes
```

#### 2. Edit the changelog

Change the headline of `[unreleased]` and use the version name.

#### 3. Merge it to Master

From the `master` branch the deployment process will finish it automatically.

----
(c) 2020, LasNQ @ Uni Hamburg
