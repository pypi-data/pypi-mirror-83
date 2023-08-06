# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mithrandir']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['lint = scripts:lint', 'test = scripts:test']}

setup_kwargs = {
    'name': 'mithrandir',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'vutr',
    'author_email': 'me@vutr.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
