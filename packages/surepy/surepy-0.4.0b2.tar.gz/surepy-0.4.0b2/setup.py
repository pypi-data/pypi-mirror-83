# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['surepy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.6.3,<4.0.0',
 'async-timeout>=3.0.1,<4.0.0',
 'colorama>=0.4.4,<0.5.0',
 'halo>=0.0.30,<0.0.31',
 'requests>=2.24.0,<3.0.0',
 'rich>=8.0.0,<9.0.0']

entry_points = \
{'console_scripts': ['surepy = surepy.cli:cli']}

setup_kwargs = {
    'name': 'surepy',
    'version': '0.4.0b2',
    'description': 'Library to interact with the flaps & doors from Sure Petcare.',
    'long_description': '# surepy\n\nLibrary & cli tool to interact with the flaps & feeders from Sure Petcare\n\nNews: *development on hold until december, sorry*\n\n## cli (alpha)\n\ncurrently implemented in master (just use it after you have read and understood the code, thanks 🐾):\n\n```bash\n  surepy cli 🐾\n\n  https://github.com/benleb/surepy\n\nOptions:\n  --version      show surepy version\n  -h, --help     Show this message and exit.\n\nCommands:\n  devices       get devices\n  locking       lock control\n  notification  get notifications\n  pets          get pets\n  report        get pet/household report\n  token         get a token\n```\n\n## library\n\ntodo: **documentation**\n',
    'author': 'Ben Lebherz',
    'author_email': 'git@benleb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benleb/surepy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
