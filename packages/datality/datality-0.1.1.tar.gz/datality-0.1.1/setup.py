# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datality']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datality',
    'version': '0.1.1',
    'description': 'this package contains implementations from the classic datastructures in the CLRS',
    'long_description': None,
    'author': 'Zetinator',
    'author_email': 'erick_zetina@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
