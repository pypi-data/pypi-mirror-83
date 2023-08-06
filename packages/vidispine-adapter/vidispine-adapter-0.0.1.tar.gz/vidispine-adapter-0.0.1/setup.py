# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vidispine']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'vidispine-adapter',
    'version': '0.0.1',
    'description': 'Python Vidispine API Adapter',
    'long_description': '# Python Vidispine Adapter\n\nA python (3.6+) wrapper around the [Vidispine API](https://apidoc.vidispine.com//latest/)\n\nNote: This is a work in progress and not all of the vidispine endpoints have been implemented yet.\n\nFull documentation coming soon\n\n\n\n## Quick start\n\n### Installation\n\n```bash\npip install vidispine-adapter\n```\n\n### Basic Usage\n\nTo use the Vidispine API you will need a to know the URL, user and password. The user does not need to be the admin user but does need the correct roles for any API call you make\n\n```python\nfrom vidispine.client import Vidispine\n\nvs = Vidispine(url=\'http://localhost:8080\', user=\'admin\', password=\'admin\')\nvs.collection.create(name=\'test_collection_1\')\n```\n\nIf `url`, `user` and `password` are not passed through when initialising, Vidispine will fall back and try and use environmental variables called `VIDISPINE_URL`, `VIDISPINE_USER` and `VIDISPINE_PASSWORD`\n```bash\nexport VIDISPINE_URL="http://localhost:8080"\nexport VIDISPINE_USER="admin"\nexport VIDISPINE_PASSWORD="admin"\n```\n\n```python\nfrom vidispine.client import Vidispine\n\nvs = Vidispine()\nvs.collection.create(name=\'test_collection_1\')\n```\n\n\n## Contributing\n\nAll contributions are welcome and appreciated. Please see [CONTRIBUTING.md](https://github.com/newmediaresearch/vidispine-adapter/blob/master/CONTRIBUTING.md) for more details including details on how to run tests etc.\n\n\n\n## Running tests\n\nThis package is setup to use the Pytest framework for testing.\nTo run tests, simply execute:\n```bash\npytest tests/\n```\nA coverage report will displayed in the shell on each test run as well as written to `htmlcov/` and can be viewed with `open htmlcov/index.html`\n\n\nCalls to Vidispine are mocked using [VCR.py](https://vcrpy.readthedocs.io/en/latest/index.html) by default but mocks can easily be refreshed and kept up to date. For more information on how to create and refresh mocks please see the `Running tests` section in [CONTRIBUTING.md](https://github.com/newmediaresearch/vidispine-adapter/blob/master/CONTRIBUTING.md).\n',
    'author': 'NMR',
    'author_email': 'developers@nmr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/newmediaresearch/vidispine-adapter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
