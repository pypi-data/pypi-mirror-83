# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cookiebutter']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'cookiecutter']

entry_points = \
{'console_scripts': ['cookiebutter = cookiebutter:wrap_cookiecutter']}

setup_kwargs = {
    'name': 'cookiebutter',
    'version': '0.0.2',
    'description': 'Cookiecutter, but all buttered up. Use cookiecutter with yaml files, or even with python files.',
    'long_description': '# cookiebutter\n\n[![PyPI](https://img.shields.io/pypi/v/cookiebutter)](https://pypi.org/project/cookiebutter/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cookiebutter)](https://pypi.org/project/cookiebutter/)\n[![PyPI License](https://img.shields.io/pypi/l/cookiebutter)](https://pypi.org/project/cookiebutter/)\n[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black/)\n\nCookiecutter, but all buttered up. Use cookiecutter with yaml files, or even with python files.\n',
    'author': 'Tom Gringauz',
    'author_email': 'tomgrin10@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomgrin10/cookiebutter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
