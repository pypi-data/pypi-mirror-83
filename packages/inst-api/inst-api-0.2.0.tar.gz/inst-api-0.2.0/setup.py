# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['instapi', 'instapi.client_api', 'instapi.models']

package_data = \
{'': ['*']}

install_requires = \
['instagram-private-api>=1.6.0,<2.0.0',
 'pillow>=7.2.0,<8.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'inst-api',
    'version': '0.2.0',
    'description': "InstAPI - comfortable and easy to use Python's library for interaction with Instagram",
    'long_description': 'InstAPI\n=============\n\n[![Code Style](https://img.shields.io/badge/Code%20Style-PEP%208-blueviolet)](https://www.python.org/dev/peps/pep-0008/) \n![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)\n[![License](https://img.shields.io/badge/License-MIT-lightgrey)](/LICENSE) \n[![Build Status](https://travis-ci.com/uriyyo/instapi.svg?branch=develop)](https://travis-ci.com/uriyyo/instapi)\n[![codecov](https://codecov.io/gh/uriyyo/instapi/branch/develop/graph/badge.svg)](https://codecov.io/gh/uriyyo/instapi)\n\n<h1 align="center">\n  <img src="/logo.svg" alt="Instapi" width="256" height="256">\n</h1>\n\nInstAPI - comfortable and easy to use Python\'s library for interaction with Instagram.\n\nInstallation\n------------\n```bash\npip install inst-api\n```\n\nUsage\n-----\nExample how to like all feeds for user\n```python\nfrom instapi import bind\nfrom instapi import User\n\nbind(\'your_username_here\', \'your_password_here\')\n\n# Get user profile by username\ninstagram_profile = User.from_username(\'username\')\n\n# Like all posts\nfor feed in instagram_profile.iter_feeds():\n  feed.like()\n```\n\nContribute\n----------\nContributions are always welcome!\n',
    'author': 'Yurii Karabas',
    'author_email': '1998uriyyo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uriyyo/instapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
