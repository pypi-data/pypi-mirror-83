# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zogutils', 'zogutils.middlewares']

package_data = \
{'': ['*']}

install_requires = \
['fastapi==0.61.1',
 'piccolo-api==0.11.0',
 'sentry-sdk==0.19.0',
 'starlette-prometheus==0.7.0']

setup_kwargs = {
    'name': 'zogutils',
    'version': '1.0.0',
    'description': "General utilities to be use in my base-fastapi template. Why ZOG? It's sound like joke and look like zoo.",
    'long_description': None,
    'author': 'Hoang Manh Tien',
    'author_email': 'tienhm.0202@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.7.7',
}


setup(**setup_kwargs)
