# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcdbot', 'mcdbot.commands', 'mcdbot.errors']

package_data = \
{'': ['*']}

install_requires = \
['aiofile>=3.1.1,<4.0.0',
 'aioredis>=1.3.1,<2.0.0',
 'asyncrcon>=1.1.4,<2.0.0',
 'discord.py>=1.5.0,<2.0.0',
 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'mcdbot',
    'version': '0.3.6',
    'description': 'My PERSONAL project for connecting Discord communities with their Minecraft servers - WIP! NO DOCUMENTATION!',
    'long_description': "# Mcdbot\n\nHello,\n\nThis is my personal project for connecting Discord communities with their Minecraft servers.\n\nI'm making this mainly for myself, and so there is no documentation about the features or installation or anything\nreally.\n\nIf you have any questions, please feel free to create an issue in the issue tracker.\n\n--jsmetana, 2020-10-17T17:18:35+02:00\n",
    'author': 'Jakub Smetana',
    'author_email': 'jakub@smetana.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/jsmetana/mcdbot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
