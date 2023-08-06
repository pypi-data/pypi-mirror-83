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
    'version': '0.0.3',
    'description': 'Automate transaction import troubles to ynab.',
    'long_description': '# YNAB -You Need a Budget\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![version](https://img.shields.io/pypi/v/ynab-import.svg)](https://pypi.org/project/ynab-import/)\n[![license](https://img.shields.io/pypi/l/ynab-import)](https://github.com/demonno/ynab-import/blob/master/LICENS\n\nBudgeting Tool helps you plan and manage your personal budget.\nIn Ynab you have budgets, each budget has one or more accounts with transactions.\n\n## Run tests\n\n    python -m pytest\n\n## How to run\n\n* Clone project\n* Create .env file in project root\n\n```ini\nSOURCE=revolut\nREAD_FROM=../statement.csv\nWRITE_TO=api\n\nYNAB_API_KEY=\nYNAB_BUDGET_ID=\n\n# ISIC\n#YNAB_ACCOUNT_ID=739410aa-0ef1-4b3e-a488-4ffe5ca3209a\n\n# Checking\nYNAB_ACCOUNT_ID=\n# Saving\n#YNAB_ACCOUNT_ID=\n```  \n\n* Run `main.py` \n\n### Developer API\n\n* https://api.youneedabudget.com/    \n    \n    \n#User API\n \n     ynab-import --s swedbank -r api -w api\n     ynab-import --s swedbank -r file.csv -w file.csv\n     ynab-import --s swedbank -r file.csv -w api\n \n Some default/extra configurations required\n \n * read-from file\n    * INPUT_FILE_PATH [default (~/{bank}.csv) home@Linux] (actual full file path required)\n * read-from api\n    * appropriate bank credentials and setup required\n    * Raise Not Supported\n * write to file \n    * OUTPUT_FILE_PATH [default (~/{bank}-ynab-{date-time}.csv) home@Linux] (add file name only if not specified)\n * write to api \n    * YNAB_API_KEY\n    * YNAB_BUDGET_ID\n\nYNAB_API_BASE_URL="https://api.youneedabudget.com/v1/"\n\n\n\n#### User Wiki\n\n\n##### Ynab \n\n####### Import Manually\n\nIts posisble to import Csv File manually\n\n\n####### Import Using Ynab API\nTo set up this integration you need to create `Personal Access Token`.\n\nGo to `https://app.youneedabudget.com/settings/developer` and click `New Token` \n',
    'author': 'demonno',
    'author_email': 'demur.nodia@gmail.com',
    'url': 'https://github.com/demonno/ynab-import',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
