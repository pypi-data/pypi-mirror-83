# evonik-test-crudl

This repo contains the python module `evonik.test.crudl`.
It is publically available on the python package index as the package `evonik-test-crudl`.

The module contains python classes to test CRUDL APIs, including REST and GQL.
It heavily used the package `evonik-dummy`, available [here](https://pypi.org/project/evonik-dummy/).



## Repo Structure

```
evonik/            # source code of evonik.test.crudl
notebooks/         # jupyter notebooks with examples and doc
LICENSE            # MIT license file
README.md          # this README
setup.py           # pypi setup script
requirements.txt   # list of dependencies for local testing / development
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `evonik.test.crudl` as the package `evonik-test-crudl`.

```bash
pip install evonik-test-crudl
```

## Test

To test the current implementation, execute the following:

```
pip install -r requirements.txt
pytest evonik/test/crudl
```

## Build & Upload

To build the package and upload a new version to pypi, execute the following commands:

```
rm -rf build dist evonik_dummy.egg-info
python3 setup.py sdist bdist_wheel --universal
twine upload dist/*
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

