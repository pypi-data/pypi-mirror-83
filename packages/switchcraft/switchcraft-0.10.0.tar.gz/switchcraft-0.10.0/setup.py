# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['switchcraft',
 'switchcraft.clients',
 'switchcraft.conversion',
 'switchcraft.conversion.arnparse',
 'switchcraft.data_classes']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.3,<2.0.0', 'pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'switchcraft',
    'version': '0.10.0',
    'description': 'Client wrappers and helpful utilities to solve common coding challenges in AWS',
    'long_description': '',
    'author': 'WWPS ProServe',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
