# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyasli', 'pyasli.browsers', 'pyasli.elements']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141,<4.0', 'webdriver-manager>=1.7,<2.0', 'wrapt>=1.11,<2.0']

setup_kwargs = {
    'name': 'pyasli',
    'version': '0.2.3',
    'description': '(Python) Yet Another Selenium Instruments',
    'long_description': None,
    'author': 'Anton Kachurin',
    'author_email': 'katchuring@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
