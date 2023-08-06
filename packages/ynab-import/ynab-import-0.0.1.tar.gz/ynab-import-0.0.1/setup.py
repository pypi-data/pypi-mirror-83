# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ynab_import',
 'ynab_import.common',
 'ynab_import.revolut',
 'ynab_import.swedbank',
 'ynab_import.ynab']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1,<8.0',
 'dataclass-csv>=1.1,<2.0',
 'dataclasses-json>=0.3.6,<0.4.0',
 'environ>=1.0,<2.0',
 'environs>=7.1,<8.0']

entry_points = \
{'console_scripts': ['ynab-import = ynab_import.main:main']}

setup_kwargs = {
    'name': 'ynab-import',
    'version': '0.0.1',
    'description': 'Automate transaction import troubles to ynab.',
    'long_description': None,
    'author': 'demonno',
    'author_email': 'demur.nodia@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
