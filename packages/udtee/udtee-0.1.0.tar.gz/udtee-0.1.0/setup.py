# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['udtee']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['udtee = udtee.cli:run']}

setup_kwargs = {
    'name': 'udtee',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Brian Pitts',
    'author_email': 'brian@polibyte.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
