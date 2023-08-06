# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygameextra_calculator']

package_data = \
{'': ['*'],
 'pygameextra_calculator': ['build/scripts-3.8/*',
                            'command/*',
                            'dist/*',
                            'pge_calculator.egg-info/*']}

install_requires = \
['pygame>=1.9.6,<2.0.0', 'pygameextra']

setup_kwargs = {
    'name': 'pygameextra-calculator',
    'version': '1.6',
    'description': 'a simple pygame extra calculator that can be ran with shell',
    'long_description': None,
    'author': 'RedstoneHair',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
