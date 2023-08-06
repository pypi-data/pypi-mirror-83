# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ergiq_fixer']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'fitparse>=1.2.0,<2.0.0', 'pytz>=2020.1,<2021.0']

entry_points = \
{'console_scripts': ['ergiq-fixer = ergiq_fixer.fitfixer:cli']}

setup_kwargs = {
    'name': 'ergiq-fixer',
    'version': '1.0.0',
    'description': 'Exports raw fit files with HR data registered as ConnectIQ into TCX for uploading',
    'long_description': None,
    'author': 'Kristian Berg',
    'author_email': 'kriberg@tihlde.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
