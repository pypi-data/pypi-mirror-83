# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zogutils', 'zogutils.middlewares']

package_data = \
{'': ['*']}

install_requires = \
['fastapi==0.61.1',
 'googletrans>=3.0.0,<4.0.0',
 'piccolo-api==0.11.0',
 'sentry-sdk==0.19.0',
 'starlette-prometheus==0.7.0']

setup_kwargs = {
    'name': 'zogutils',
    'version': '1.2.2',
    'description': "General utilities to be use in my base-fastapi template. Why ZOG? It's sound like joke and look like zoo.",
    'long_description': '# ZOG Utils\n\nUtilities to use in my base-api project template. https://github.com/tienhm0202/base-fastapi/\n\nWhy ZOG? Because I can\'t named it as `utils` only, so I have to add a prefix.\nZOG sounds like `joke` and looks like `zoo`. I found that funny enough to use.\n\n# Usage\n\n```bash\n$ pip install zogutils\n```\n\n## To generate short unique id string\n\n```python\nfrom zogutils import secret\n\nsecret.unique_id(8, "ID_")\n# return: ID_a7uFg9k0\n```\n\n## To shorten package name like Java\'s Logback\n\n```python\nfrom zogutils import package_name\n\npackage_name.shorten("company.scope.modules.Function", 9)\n# return: (something like) c.s.m.Function - depends on max length\n```\n\n## To init some middlewares\n\n```python\nfrom zogutils import middlewares\nfrom your.app import settings, fastapi_app\n\nmiddlewares.init_app(fastapi_app, settings)\n```\n\n### Configs:\n\n```\n# Sentry\nSENTRY_DSN: Optional[HttpUrl] = None\nSENTRY_INCLUDE: Optional[List[str]] = ["src"]\nSENTRY_SAMPLE_RATE: Optional[float] = 0.5\n\n# CSRF\nSECURITY_CSRF: bool = False\n\n# Rate limit\nRATE_LIMIT: int = 100\nRATE_LIMIT_TIME_SPAN: int = 30\nRATE_LIMIT_BLOCK_DURATION: int = 300\n\n# Prometheus\nPROMETHEUS_ENABLE: bool = True\nPROMETHEUS_PATH: str = "/metrics/"\n\n# Cors\nBACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []\n```',
    'author': 'Hoang Manh Tien',
    'author_email': 'tienhm.0202@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tienhm0202/zogutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<3.8.0',
}


setup(**setup_kwargs)
