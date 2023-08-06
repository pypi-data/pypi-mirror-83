# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchmtl', 'torchmtl.tests']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2,<4.0.0',
 'networkx>=2.5,<3.0',
 'scipy>=1.5.3,<2.0.0',
 'torch>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'torchmtl',
    'version': '0.1.0',
    'description': 'A lightweight module for Multi-Task Learning in pytorch',
    'long_description': None,
    'author': 'Christian Bock',
    'author_email': 'christian.bock@bsse.ethz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
