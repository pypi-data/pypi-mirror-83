# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lyrix']

package_data = \
{'': ['*'], 'lyrix': ['assets/*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'certifi>=2020.6.20,<2021.0.0',
 'chardet>=3.0.4,<4.0.0',
 'idna>=2.10,<3.0',
 'lyricsgenius>=2.0.2,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'six>=1.15.0,<2.0.0',
 'spotipy>=2.16.1,<3.0.0',
 'urllib3>=1.25.11,<2.0.0']

setup_kwargs = {
    'name': 'lyrix',
    'version': '0.1.0',
    'description': 'The ultimate lyrics app for tiling window managers.',
    'long_description': None,
    'author': 'Daniel Rose',
    'author_email': 'daniel@whitehatcat.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
