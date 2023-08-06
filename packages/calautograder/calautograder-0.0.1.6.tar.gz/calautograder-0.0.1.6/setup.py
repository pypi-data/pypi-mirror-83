# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calautograder',
 'calautograder.entry',
 'calautograder.project',
 'calautograder.project.freezerestore']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['calautograder = entry:main']}

setup_kwargs = {
    'name': 'calautograder',
    'version': '0.0.1.6',
    'description': 'commandline autograder implimentation',
    'long_description': None,
    'author': 'Nick Brown',
    'author_email': 'bicknrown@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
