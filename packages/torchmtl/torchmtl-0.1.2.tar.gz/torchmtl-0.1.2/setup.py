# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchmtl']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2,<4.0.0',
 'networkx>=2.5,<3.0',
 'scipy>=1.5.3,<2.0.0',
 'torch>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'torchmtl',
    'version': '0.1.2',
    'description': 'A lightweight module for Multi-Task Learning in pytorch',
    'long_description': '![alt text](https://github.com/chrisby/torchMTL/blob/main/torchmtl_logo.png "torchMTL Logo")    \nA lightweight module for Multi-Task Learning in pytorch.\n\n`torchmtl` tries to help you composing modular multi-task architectures with minimal effort. All you need is a list of dictionaries in which you define your layers and how they build on each other. From this, `torchmtl` constructs a meta-computation graph which is executed in each forward pass of the created `MTLModel`. To combine outputs from multiple layers, simple [wrapper functions](https://github.com/chrisby/torchMTL/blob/main/torchmtl/wrapping_layers.py) are provided.\n\n### Installation\n`torchmtl` can be installed via `pip`:\n```\npip install torchmtl\n```\n\n### Quickstart\nAssume you want to use two different embeddings of your input, combine them and then solve different prediction tasks.\n',
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
