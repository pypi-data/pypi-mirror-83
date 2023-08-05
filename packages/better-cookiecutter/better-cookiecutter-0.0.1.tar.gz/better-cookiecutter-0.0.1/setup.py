# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['better_cookiecutter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'better-cookiecutter',
    'version': '0.0.1',
    'description': 'Use cookiecutter with yaml files, or even with python files',
    'long_description': '# better-cookiecutter\n\n[![PyPI](https://img.shields.io/pypi/v/better-cookiecutter)](https://pypi.org/project/better-cookiecutter/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/better-cookiecutter)](https://pypi.org/project/better-cookiecutter/)\n[![PyPI License](https://img.shields.io/pypi/l/better-cookiecutter)](https://pypi.org/project/better-cookiecutter/)\n[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black/)\n\nUse cookiecutter with yaml files, or even with python files.\n\n',
    'author': 'Tom Gringauz',
    'author_email': 'tomgrin10@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomgrin10/better-cookiecutter',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
