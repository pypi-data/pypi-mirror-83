# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['worldcoinapi']
setup_kwargs = {
    'name': 'worldcoinapi',
    'version': '1.0.0',
    'description': 'API for WorldCoin (https://vk.com/app7614516)',
    'long_description': None,
    'author': 'Timtaran',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
