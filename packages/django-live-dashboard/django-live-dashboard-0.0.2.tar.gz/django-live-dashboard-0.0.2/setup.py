# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_live_dashboard']

package_data = \
{'': ['*'],
 'django_live_dashboard': ['static/*', 'templates/django_live_dashboard/*']}

install_requires = \
['aredis>=1.1.8,<2.0.0', 'pydantic>=1.6.1,<2.0.0', 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'django-live-dashboard',
    'version': '0.0.2',
    'description': 'Live runtime metrics dashboard for Django',
    'long_description': None,
    'author': 'shen',
    'author_email': 'dustet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6,<4',
}


setup(**setup_kwargs)
