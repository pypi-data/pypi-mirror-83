# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dj_pony', 'dj_pony.hashedfield']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2']

setup_kwargs = {
    'name': 'dj-pony.hashedfield',
    'version': '0.1.0',
    'description': 'A Hashed Field for Django that does all the work for you.',
    'long_description': None,
    'author': 'Samuel Bishop',
    'author_email': 'sam@techdragon.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
