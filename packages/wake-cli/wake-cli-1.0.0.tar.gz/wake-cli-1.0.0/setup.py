# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['wake']
install_requires = \
['docopt>=0.6.2,<0.7.0', 'paramiko>=2.7.2,<3.0.0', 'wakeonlan>=1.1.6,<2.0.0']

entry_points = \
{'console_scripts': ['wake = wake:cli']}

setup_kwargs = {
    'name': 'wake-cli',
    'version': '1.0.0',
    'description': 'Wake brings together your ssh config and WakeOnLan together, so you can use the same aliases you use to ssh to your machines, to wake them up.',
    'long_description': None,
    'author': 'James Stidard',
    'author_email': 'james@stidard.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
