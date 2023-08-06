# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['msn',
 'msn.core',
 'msn.message',
 'msn.nlp',
 'msn.page',
 'msn.profile',
 'msn.token',
 'msn.user',
 'msn.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24,<3.0']

setup_kwargs = {
    'name': 'msn',
    'version': '1.0.2',
    'description': '',
    'long_description': None,
    'author': 'Oscar Giraldo Castillo',
    'author_email': 'oscar.gi.cast@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
