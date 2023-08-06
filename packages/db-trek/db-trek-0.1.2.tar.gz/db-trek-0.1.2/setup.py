# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trek']

package_data = \
{'': ['*'], 'trek': ['templates/*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'pyodbc>=4.0.30,<5.0.0', 'structlog>=20.1.0,<21.0.0']

entry_points = \
{'console_scripts': ['trek = trek.main:main']}

setup_kwargs = {
    'name': 'db-trek',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Jon Katsini',
    'author_email': 'jon@greeff-katsini.co.za',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mr-katsini/trek',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
