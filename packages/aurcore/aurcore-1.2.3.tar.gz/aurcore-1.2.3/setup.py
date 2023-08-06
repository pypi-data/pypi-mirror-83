# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aurcore', 'aurcore.event', 'aurcore.log', 'aurcore.util']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aurcore',
    'version': '1.2.3',
    'description': 'Aurcore!',
    'long_description': None,
    'author': 'Zenith',
    'author_email': 'z@zenith.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
