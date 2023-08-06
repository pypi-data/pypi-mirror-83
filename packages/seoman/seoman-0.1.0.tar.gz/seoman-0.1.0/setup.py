# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seoman', 'seoman.utils']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=1.10.1,<2.0.0',
 'google-auth-oauthlib>=0.4.1,<0.5.0',
 'halo>=0.0.30,<0.0.31',
 'inquirer>=2.7.0,<3.0.0',
 'pyexcelerate>=0.9.0,<0.10.0',
 'pytablewriter>=0.58.0,<0.59.0',
 'requests>=2.24.0,<3.0.0',
 'toml>=0.10.1,<0.11.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['seoman = seoman.main:app']}

setup_kwargs = {
    'name': 'seoman',
    'version': '0.1.0',
    'description': 'A CLI tool for technical SEOs',
    'long_description': None,
    'author': 'seo.do',
    'author_email': 'yagizcan@zeo.org',
    'maintainer': 'Yagiz Degirmenci',
    'maintainer_email': 'yagizcan@zeo.org',
    'url': 'https://seo.do/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
