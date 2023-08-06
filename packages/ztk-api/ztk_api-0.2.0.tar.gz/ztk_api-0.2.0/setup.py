# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ztk_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4',
 'dataclasses-json>=0.5,<0.6',
 'pydantic>=1.6,<1.7',
 'requests>=2.24,<2.25',
 'structlog>=20,<21']

setup_kwargs = {
    'name': 'ztk-api',
    'version': '0.2.0',
    'description': '折淘客接口',
    'long_description': '# WARNING\nthis is only for internal use (use at your own risk)\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
