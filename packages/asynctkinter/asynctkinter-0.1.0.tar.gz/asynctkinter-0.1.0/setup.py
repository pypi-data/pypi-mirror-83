# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asynctkinter']

package_data = \
{'': ['*']}

install_requires = \
['asyncgui>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'asynctkinter',
    'version': '0.1.0',
    'description': "async library that works on top of tkinter's event loop",
    'long_description': None,
    'author': 'Nattōsai Mitō',
    'author_email': 'flow4re2c@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
