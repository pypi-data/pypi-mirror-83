# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hsc_assembler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hsc-assembler',
    'version': '0.1.0',
    'description': 'Assembler for the hsc (name TBD) ISA (https://github.com/HomebrewSiliconClub/Processor)',
    'long_description': None,
    'author': 'Bolun Thompson',
    'author_email': 'abolunthompson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
