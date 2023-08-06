# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jsconfpy']
setup_kwargs = {
    'name': 'jsconfpy',
    'version': '1.3.0',
    'description': 'json save config - это библиотека легкого задания конфигурационных файлов',
    'long_description': None,
    'author': 'iHelper',
    'author_email': 'pettorr.lu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
