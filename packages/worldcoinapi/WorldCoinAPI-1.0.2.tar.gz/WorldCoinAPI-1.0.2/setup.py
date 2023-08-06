# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['worldcoinapi']
install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'worldcoinapi',
    'version': '1.0.2',
    'description': 'API for WorldCoin (https://vk.com/app7614516)',
    'long_description': None,
    'author': 'Timtaran',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
