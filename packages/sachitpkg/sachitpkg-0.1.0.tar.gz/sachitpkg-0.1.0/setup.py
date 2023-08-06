# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sachitpkg']

package_data = \
{'': ['*']}

install_requires = \
['pyspark>=3.0.1,<4.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'sachitpkg',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
