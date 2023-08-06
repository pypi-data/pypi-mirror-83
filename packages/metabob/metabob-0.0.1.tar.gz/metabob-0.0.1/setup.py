# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['metabob']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'metabob',
    'version': '0.0.1',
    'description': 'Metabob pkg/cli',
    'long_description': None,
    'author': 'jessekrubin',
    'author_email': 'jessekrubin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
