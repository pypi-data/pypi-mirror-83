# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ghworkspace']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.53,<2.0']

setup_kwargs = {
    'name': 'ghworkspace',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'm3y',
    'author_email': 'ma3ya.ozw+pypi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
