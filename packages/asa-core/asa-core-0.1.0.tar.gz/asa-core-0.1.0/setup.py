# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asa_core']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.3,<2.0.0', 'pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'asa-core',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Derek Sudduth',
    'author_email': 'derek.sudduth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
