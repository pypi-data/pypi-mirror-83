# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brain_games', 'brain_games.scripts']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['brain-games = brain_games.scripts.brain_games:main']}

setup_kwargs = {
    'name': 'hexlet-code',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Алексей Малышев',
    'author_email': 'alexey1978malyshev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
