# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydub-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydub-stubs',
    'version': '0.24.1.0',
    'description': 'Stub-only package containing type information for pydub',
    'long_description': None,
    'author': 'SeparateRecords',
    'author_email': 'me@rob.ac',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SeparateRecords/pydub-stubs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
