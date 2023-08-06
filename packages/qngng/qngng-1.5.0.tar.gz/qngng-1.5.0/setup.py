# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qngng']

package_data = \
{'': ['*'], 'qngng': ['cats/*']}

entry_points = \
{'console_scripts': ['qngng = qngng.qngng:_main']}

setup_kwargs = {
    'name': 'qngng',
    'version': '1.5.0',
    'description': 'The Queb name generator: next generation',
    'long_description': None,
    'author': 'Philippe Proulx',
    'author_email': 'eeppeliteloop@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eepp/qngng/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
