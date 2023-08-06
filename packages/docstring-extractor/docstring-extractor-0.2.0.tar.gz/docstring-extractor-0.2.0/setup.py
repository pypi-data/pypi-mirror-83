# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['docstring_extractor']
setup_kwargs = {
    'name': 'docstring-extractor',
    'version': '0.2.0',
    'description': 'Get Python docstrings from files',
    'long_description': '# docstring-extractor\n\nGet Python docstrings from files or Python source code.\n\nExample usage:\n\n```python\n>>> from docstring_extractor import get_docstrings\n>>>\n>>> with open("example.py") as file:\n...     get_docstrings(file)\n...\n\n{\n    \'module\': \'example\',\n    \'content\': [{\n        \'type\': \'Function\',\n        \'name\': \'my_fuction\',\n        \'line\': 4,\n        \'docstring\': \'Long description spanning multiple lines\\n- First line\\n- Second line\\n- Third line\\n\\n:param name: description 1\\n:param int priority: description 2\\n:param str sender: description 3\\n:raises ValueError: if name is invalid\'\n    }]\n}\n```\n\n# Contributing\n\nThis project uses [Black](https://github.com/psf/black).\n',
    'author': 'Francisco Jimenez Cabrera',
    'author_email': 'jkfran@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jkfran/docstring-extractor',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
