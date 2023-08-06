# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vvs_portal_gun']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['vvs-portal-gun = vvs_portal_gun.main:app']}

setup_kwargs = {
    'name': 'vvs-portal-gun',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Portal Gun\n\nThe awesome Portal Gun',
    'author': 'Vikash_Vikram',
    'author_email': 'Vikash_Vikram@external.mckinsey.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
