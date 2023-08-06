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
    'version': '0.2.3.1',
    'description': '(Python) Yet Another Selenium Instruments',
    'long_description': '## Pyasli\n[![coverage report](https://gitlab.com/outcatcher/pyasli/badges/master/coverage.svg)](https://outcatcher.gitlab.io/pyasli/)\n[![pipeline status](https://gitlab.com/outcatcher/pyasli/badges/master/pipeline.svg)](https://gitlab.com/outcatcher/pyasli/commits/master)\n\n### Simple selenium python wrapper\n\n#### There are two ways to use browser:\n\n##### Use default shared driver:\n\n```python\nfrom pyasli.browsers import browser\n\nbrowser.base_url = "https://the-internet.herokuapp.com"\nbrowser.open("/disappearing_elements")\nelement1 = browser.element("div.example p")\nassert element1.get_actual() is element1.get_actual(), "Element is found 2 times"\n```\n\n##### Use exact driver (can be used as context manager):\n```python\nfrom tests.conftest import browser_instance\n\nwith browser_instance(base_url="https://the-internet.herokuapp.com") as browser:\n    browser.open("/disappearing_elements")\n    element1 = browser.element("div.example p")\n    assert element1.get_actual() is element1.get_actual(), "Element is found 2 times"\n```\n\nIn case `browser_instance` is used as context manager, all browser windows will be closed at\nexiting context\n\n----\n\n##### There is no documentation currently. For usage please refer to tests\n\n----\n\nBuilt wheels are available at https://pypi.outcatcher.com/simple/pyasli/\n\n_<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" \t\t\t    title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" \t\t\t    title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>_\n',
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
