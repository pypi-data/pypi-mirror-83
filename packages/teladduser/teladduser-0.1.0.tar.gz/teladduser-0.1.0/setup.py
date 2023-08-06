# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['teladduser']

package_data = \
{'': ['*']}

install_requires = \
['Telethon>=1.16.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'defusedxml>=0.6.0,<0.7.0',
 'openpyxl>=3.0.5,<4.0.0',
 'python-decouple>=3.3,<4.0',
 'rows[xlsx]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['teladduser = teladduser.teladduser:teladduser']}

setup_kwargs = {
    'name': 'teladduser',
    'version': '0.1.0',
    'description': 'This is a CLI with the aim to add new users from a spreadsheet at a Telegram supergroup.',
    'long_description': '# teladduser\nThis is a CLI with the aim to add new users from a spreadsheet at a Telegram supergroup.\n',
    'author': 'Vicente Marçal',
    'author_email': 'vicente.marcal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
