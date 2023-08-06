# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['konfik']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'rich>=9.1.0,<10.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['konfik = konfik:cli_entrypoint']}

setup_kwargs = {
    'name': 'konfik',
    'version': '2.0.0',
    'description': 'The Strangely Familiar Config Parser',
    'long_description': None,
    'author': 'rednafi',
    'author_email': 'redowan.nafi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
