# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyadr', 'pyadr.assets', 'pyadr.cli', 'pyadr.git', 'pyadr.git.cli']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0,<1', 'gitpython>=3.1,<4.0', 'loguru>=0,<1', 'python-slugify>=4,<5']

extras_require = \
{':python_version < "3.7"': ['importlib_resources>=1.4.0,<2.0.0'],
 'bdd': ['behave4git>=0,<1', 'PyHamcrest>=2.0,<3.0'],
 'docs': ['sphinx>=2.3,<3.0',
          'sphinx-autodoc-typehints>=1.10,<2.0',
          'sphinx-autobuild>=0,<1',
          'sphinx_rtd_theme>=0,<1',
          'm2r>=0,<1'],
 'format': ['isort>=5,<6', 'seed-isort-config>=2.2,<3.0', 'black'],
 'lint': ['flake8>=3.7,<4.0',
          'flake8-bugbear>=20,<21',
          'pydocstyle>=5.0,<6.0',
          'pylint>=2.3,<3.0',
          'yapf>=0,<1'],
 'repl': ['bpython>=0,<1'],
 'test': ['pytest>=6.1,<7.0',
          'pytest-cov>=2.8,<3.0',
          'pytest-mock>=3.2,<4.0',
          'pytest-html>=2.0,<3.0',
          'pytest-asyncio>=0,<1',
          'PyHamcrest>=2.0,<3.0'],
 'type': ['mypy>=0,<1']}

entry_points = \
{'console_scripts': ['git-adr = pyadr.git.cli:main', 'pyadr = pyadr.cli:main']}

setup_kwargs = {
    'name': 'pyadr',
    'version': '0.17.0',
    'description': 'CLI to help with an ADR process lifecycle (proposal/approval/rejection/deprecation/superseeding), which used git.',
    'long_description': None,
    'author': 'Emmanuel Sciara',
    'author_email': 'emmanuel.sciara@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/opinionated-digital-center/pyadr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
