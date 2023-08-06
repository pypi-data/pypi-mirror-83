# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ptonppl']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.10.0,<2.0.0',
 'bs4>=0.0.1,<0.0.2',
 'click-option-group>=0.5.1,<0.6.0',
 'click>=7.1.2,<8.0.0',
 'click_help_colors>=0.8,<0.9',
 'python-ldap>=3.3.1,<4.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['ptonppl = ptonppl.__main__:main']}

setup_kwargs = {
    'name': 'ptonppl',
    'version': '1.0.2',
    'description': 'An integration package to lookup Princeton campus users.',
    'long_description': "# ptonppl — Princeton People\n\nThis provides a Python package and a command-line tool to lookup the\ncampus directory of any member of the Princeton community. The package\nprovides a unified search function that queries the following fields:\n- PUID, *e.g.*, `902312554`\n- NetID, *e.g.*, `lumbroso`\n- Alias, when the user has defined one, *e.g.*, `jeremie.lumbroso`\n- Email, *e.g.*, `lumbroso@princeton.edu`\n\nThis information is hard to come by consistently, and this tool seeks\nto provide a robust interface to the information.\n\n## Installation\n\nThe package is distributed on PyPI and can be installed using the usual\ntools, such as `pip` or `pipenv`:\n```shell\n$ pip install --user ptonppl\n```\n\n## Help Message\n\n```\n$ ptonppl --help\n\nUsage: ptonppl [OPTIONS] [QUERY]...\n\n  Lookup the directory information (PUID, NetID, email, name) of any\n  Princeton campus person, using whichever of LDAP, web directory or proxy\n  server is available.\n\nOptions:\n  -t, --type TYPE               Output type (e.g.: term, json, csv, emails).\n  -u, --uniq / -nu, --not-uniq  Filter out duplicate records from the output.\n  -s, --stats                   Display statistics once processing is done.\n  -i, --input FILENAME          Read input from a file stream.\n  -f, --fields FIELDS           Fields to keep (e.g.: 'puid,netid,email').\n  --header / -nh, --no-header   Include or remove header in output.\n  --version                     Show the version and exit.\n  --help                        Show this message and exit.\n\n```\n\n## License\n\nThis project is licensed under the LGPLv3 license, with the understanding\nthat importing a Python modular is similar in spirit to dynamically linking\nagainst it.\n\n- You can use the library `ptonppl` in any project, for any purpose, as long\n  as you provide some acknowledgement to this original project for use of\n  the library.\n\n- If you make improvements to `ptonppl`, you are required to make those\n  changes publicly available.",
    'author': 'Jérémie Lumbroso',
    'author_email': 'lumbroso@cs.princeton.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jlumbroso/ptonppl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
