# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polaroid']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'polaroid',
    'version': '0.2.0',
    'description': 'Hyper Fast and safe image manipulation library for python . Powered by rust. ',
    'long_description': None,
    'author': 'Arnav Jindal',
    'author_email': '60603110+Daggy1234@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
