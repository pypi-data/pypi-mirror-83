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
    'version': '0.0.4',
    'description': 'the reference compiler for the Crowbar programming language',
    'long_description': "the reference compiler for the [Crowbar](https://sr.ht/~boringcactus/crowbar-lang/) language.\n\nrequirements:\n* [QBE](https://c9x.me/compile/) installed somewhere on your PATH\n* gcc\n\nusage (i probably will forget to update this so [check directly](https://git.sr.ht/~boringcactus/crowbar-reference-compiler/tree/main/crowbar_reference_compiler/__init__.py)):\n```\nusage: crowbarc-reference [-h] [-V] [-g] [--stop-at-parse-tree]\n                          [--stop-at-qbe-ssa] [-S] [-o OUT]\n                          input\n\nThe reference compiler for the Crowbar programming language\n\npositional arguments:\n  input                 input file\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -V, --version         show program's version number and exit\n  -g, --include-debug-info\n  --stop-at-parse-tree\n  --stop-at-qbe-ssa\n  -S, --stop-at-assembly\n  -o OUT, --out OUT     output file\n```\n",
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
