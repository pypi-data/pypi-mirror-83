# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*'], 'src': ['templates/*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'pyodbc>=4.0.30,<5.0.0', 'structlog>=20.1.0,<21.0.0']

setup_kwargs = {
    'name': 'db-trek',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jon Katsini',
    'author_email': 'jon@greeff-katsini.co.za',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mr-katsini/Trek',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
