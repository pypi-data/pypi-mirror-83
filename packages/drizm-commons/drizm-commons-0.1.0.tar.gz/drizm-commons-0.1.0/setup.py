# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drizm_commons', 'drizm_commons.sqla']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy==1.3.20']

setup_kwargs = {
    'name': 'drizm-commons',
    'version': '0.1.0',
    'description': 'Python3 commons for the Drizm organization',
    'long_description': '# Python Commons\n\nThis package includes shared code used by\nthe Drizm organizations development team.  \n\nIt is not intended for public usage but you\nmay still download, redistribute or \nmodify it to your liking.\n\n## Usage\n\nInstall:  \n>pip install drizm-commons\n\nImport like so:  \nimport drizm_commons\n',
    'author': 'ThaRising',
    'author_email': 'kochbe.ber@gmail.com',
    'maintainer': 'Dominik Lewandowski',
    'maintainer_email': 'dominik.lewandow@gmail.com',
    'url': 'https://github.com/drizm-team/python-commons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
