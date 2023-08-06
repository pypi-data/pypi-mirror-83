# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protos', 'protos.estimators']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'protos',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tomas Pereira de Vasconcelos',
    'author_email': 'tomas@tiqets.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
