# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roomie_bot',
 'roomie_bot.api_rest',
 'roomie_bot.database',
 'roomie_bot.expenses']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1.2,<2.0.0', 'python-telegram-bot>=12.8,<13.0']

setup_kwargs = {
    'name': 'roomie-bot',
    'version': '0.1.0',
    'description': 'Telegram bot with utilities for roommates',
    'long_description': None,
    'author': 'Dipzza',
    'author_email': 'dipzza@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
