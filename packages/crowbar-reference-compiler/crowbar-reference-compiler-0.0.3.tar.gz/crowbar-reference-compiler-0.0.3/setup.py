# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crowbar_reference_compiler']

package_data = \
{'': ['*']}

install_requires = \
['parsimonious>=0.8.1,<0.9.0', 'regex>=2020.10.11,<2021.0.0']

entry_points = \
{'console_scripts': ['crowbarc-reference = crowbar_reference_compiler:main']}

setup_kwargs = {
    'name': 'crowbar-reference-compiler',
    'version': '0.0.3',
    'description': 'the reference compiler for the Crowbar programming language',
    'long_description': '',
    'author': 'Melody Horn',
    'author_email': 'melody@boringcactus.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.sr.ht/~boringcactus/crowbar-reference-compiler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
