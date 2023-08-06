# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fwmp3']
setup_kwargs = {
    'name': 'fwmp3',
    'version': '1.0.0',
    'description': 'python 3.8',
    'long_description': None,
    'author': 'John Smith',
    'author_email': 'azarovnick@bk.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
