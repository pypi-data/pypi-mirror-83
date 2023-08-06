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
    'version': '0.0.2',
    'description': 'Composable kernels for scikit-learn implemented in JAX.',
    'long_description': '# sklearn-jax-kernels\n\n[![Build Status](https://travis-ci.com/ExpectationMax/sklearn-jax-kernels.svg?token=3sUUnmMzs9wxN3Qapssj&branch=master)](https://travis-ci.com/ExpectationMax/sklearn-jax-kernels)\n\n**Warning: This project is still in an early stage it could be that the API\nwill change in the future, further functionality is still very limited to the\nuse cases which defined the creation of the project (application to DNA\nsequences present in Biology).**\n\n## Why?\nEver wanted to run a kernel-based model from\n[scikit-learn](https://scikit-learn.org/) on a relatively large dataset?  If so\nyou will have noticed, that this can take extraordinarily long and require huge\namounts of memory, especially if you are using compositions of kernels (such as\nfor example `k1 * k2 + k3`).  This is due to the way Kernels are computed in\nscikit-learn: For each kernel, the complete kernel matrix is computed, and the\ncompositions are then computed from the kernel matrices.  Further,\n`scikit-learn` does not rely on an automatic differentiation framework for the\ncomputation of gradients though kernel operations.\n\n## Introduction\n\n`sklearn-jax-kernels` was designed to circumvent these issues:\n\n - The utilization of [JAX](https://github.com/google/jax) allows accelerating\n   kernel computations through [XLA](https://www.tensorflow.org/xla)\n   optimizations, computation on GPUs and simplifies the computation of\n   gradients though kernels\n - The composition of kernels takes place on a per-element basis, such that\n   unnecessary copies can be optimized away by JAX compilation\n\nThe goal of `sklearn-jax-kernels` is to provide the same flexibility and ease\nof use as known from `scikit-learn` kernels while improving speed and allowing\nthe faster design of new kernels through Automatic Differentiation.\n\nThe kernels in this package follow the [scikit-learn kernel\nAPI](https://scikit-learn.org/stable/modules/gaussian_process.html#gaussian-process-kernel-api).\n\n## Quickstart\n\nA short demonstration of how the kernels can be used, inspired by the\n[ scikit-learn\ndocumentation](https://scikit-learn.org/stable/auto_examples/gaussian_process/plot_gpc_iris.html).\n\n```python\nfrom sklearn import datasets\nimport jax.numpy as jnp\nfrom sklearn_jax_kernels import RBF, GaussianProcessClassifier\n\niris = datasets.load_iris()\nX = jnp.asarray(iris.data)\ny = jnp.array(iris.target, dtype=int)\n\nkernel = 1. + RBF(length_scale=1.0)\ngpc = GaussianProcessClassifier(kernel=kernel).fit(X, y)\n```\n\nHere a further example demonstrating how kernels can be combined:\n\n```python\nfrom sklearn_jax_kernels.base_kernels import RBF, NormalizedKernel\nfrom sklearn_jax_kernels.structured.strings import SpectrumKernel\n\nmy_kernel = RBF(1.) * SpectrumKernel(n_gram_length=3)\nmy_kernel_2 = RBF(1.) + RBF(2.)\nmy_kernel_2 = NormalizedKernel(my_kernel_2)\n```\n\nSome further inspiration can be taken from the tests in the subfolder `tests`.\n\n## Implemented Kernels\n\n - Kernel compositions ($+,-,*,/$, exponentiation)\n - Kernels for real valued data:  \n     - RBF kernel\n - Kernels for same length strings:  \n     - SpectrumKernel\n     - DistanceSpectrumKernel, SpectrumKernel with distance weight between\n       matching substrings\n     - ReverseComplement Spectrum kernel (relevant for applications in Biology\n       when working with DNA sequences)\n\n## TODOs\n\n - Implement more fundamental Kernels\n - Implement jax compatible version of GaussianProcessRegressor\n - Optimize GaussianProcessClassifier for performance\n - Run benchmarks to show benefits in speed\n - Add fake "split" kernel which allows to apply different kernels to different\n   parts of the input\n',
    'author': 'Max Horn',
    'author_email': 'max.horn@bsse.ethz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ExpectationMax/sklearn-jax-kernels',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
