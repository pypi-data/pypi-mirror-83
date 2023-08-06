# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sklearn_jax_kernels', 'sklearn_jax_kernels.structured']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.1.59,<0.2.0', 'jaxlib>=0.1.40,<0.2.0', 'scikit-learn>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'sklearn-jax-kernels',
    'version': '0.0.1',
    'description': 'Composable kernels for scikit-learn implemented in JAX.',
    'long_description': None,
    'author': 'Max Horn',
    'author_email': 'max.horn@bsse.ethz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
