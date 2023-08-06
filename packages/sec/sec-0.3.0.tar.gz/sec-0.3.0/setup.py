# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sec']
setup_kwargs = {
    'name': 'sec',
    'version': '0.3.0',
    'description': 'Tiny Python library for secrets',
    'long_description': None,
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@sourcelair.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
