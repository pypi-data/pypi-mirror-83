# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ezsql']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ezsql',
    'version': '0.1.0',
    'description': '',
    'long_description': '# ezsql\n',
    'author': 'guaifish',
    'author_email': 'guaifish@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guaifish/ezsql',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
