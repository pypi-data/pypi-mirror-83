# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['docstring_extractor']
setup_kwargs = {
    'name': 'docstring-extractor',
    'version': '0.1.0',
    'description': 'Get Python docstrings from files',
    'long_description': None,
    'author': 'Francisco Jimenez Cabrera',
    'author_email': 'jkfran@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
