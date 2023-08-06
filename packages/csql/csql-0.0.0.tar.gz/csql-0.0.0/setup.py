# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csql', 'csql.models', 'csql.renderer']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 'pandas': ['pandas>=1,<2']}

setup_kwargs = {
    'name': 'csql',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Jarrad Whitaker',
    'author_email': 'akdor1154@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
