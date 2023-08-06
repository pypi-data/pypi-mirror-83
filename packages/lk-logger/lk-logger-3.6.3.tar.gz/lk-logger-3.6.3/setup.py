# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lk_logger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lk-logger',
    'version': '3.6.3',
    'description': 'Advanced logger with source code lineno indicator.',
    'long_description': None,
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
