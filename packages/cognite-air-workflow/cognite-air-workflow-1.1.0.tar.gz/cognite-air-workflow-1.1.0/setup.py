# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite',
 'cognite.airworkflow',
 'cognite.airworkflow.model',
 'cognite.airworkflow.util']

package_data = \
{'': ['*'], 'cognite.airworkflow': ['schemas/*']}

install_requires = \
['PyGithub>=1.51,<2.0',
 'bandit>=1.6.2,<2.0.0',
 'black>=19.10b0,<20.0',
 'cerberus>=1.3.2,<2.0.0',
 'cognite-sdk-experimental>=0,<1',
 'cognite-sdk>=2,<3',
 'croniter>=0.3.31,<0.4.0',
 'flake8>=3.8.3,<4.0.0',
 'gitpython>=3.1.1,<4.0.0',
 'isort>=5.5.2,<6.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'mypy>=0.782,<0.783',
 'pre-commit>=2.7.1,<3.0.0',
 'pyjwt>=1.7.1,<2.0.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'pytest-custom_exit_code>=0.3.0,<0.4.0',
 'pytest>=6.0.1,<7.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'ruptures>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'cognite-air-workflow',
    'version': '1.1.0',
    'description': 'Client library to perform all required cognite airflow functions built to function with AIR CDF',
    'long_description': None,
    'author': 'Arun Kaashyap Arunachalam',
    'author_email': 'arun.arunachalam@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
