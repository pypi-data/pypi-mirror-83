# Python Vidispine Adapter

A python (3.6+) wrapper around the [Vidispine API](https://apidoc.vidispine.com//latest/)

Note: This is a work in progress and not all of the vidispine endpoints have been implemented yet.

Full documentation coming soon



## Quick start

### Installation

```bash
pip install vidispine-adapter
```

### Basic Usage

To use the Vidispine API you will need a to know the URL, user and password. The user does not need to be the admin user but does need the correct roles for any API call you make

```python
from vidispine.client import Vidispine

vs = Vidispine(url='http://localhost:8080', user='admin', password='admin')
vs.collection.create(name='test_collection_1')
```

If `url`, `user` and `password` are not passed through when initialising, Vidispine will fall back and try and use environmental variables called `VIDISPINE_URL`, `VIDISPINE_USER` and `VIDISPINE_PASSWORD`
```bash
export VIDISPINE_URL="http://localhost:8080"
export VIDISPINE_USER="admin"
export VIDISPINE_PASSWORD="admin"
```

```python
from vidispine.client import Vidispine

vs = Vidispine()
vs.collection.create(name='test_collection_1')
```


## Contributing

All contributions are welcome and appreciated. Please see [CONTRIBUTING.md](https://github.com/newmediaresearch/vidispine-adapter/blob/master/CONTRIBUTING.md) for more details including details on how to run tests etc.



## Running tests

This package is setup to use the Pytest framework for testing.
To run tests, simply execute:
```bash
pytest tests/
```
A coverage report will displayed in the shell on each test run as well as written to `htmlcov/` and can be viewed with `open htmlcov/index.html`


Calls to Vidispine are mocked using [VCR.py](https://vcrpy.readthedocs.io/en/latest/index.html) by default but mocks can easily be refreshed and kept up to date. For more information on how to create and refresh mocks please see the `Running tests` section in [CONTRIBUTING.md](https://github.com/newmediaresearch/vidispine-adapter/blob/master/CONTRIBUTING.md).
