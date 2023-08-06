# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_utils']

package_data = \
{'': ['*']}

install_requires = \
['rich>=9.1.0,<10.0.0']

setup_kwargs = {
    'name': 'rich-utils',
    'version': '0.4.0',
    'description': 'Utility methods and classes for the "rich" package.',
    'long_description': '# rich-utils\n\n[![CircleCI](https://circleci.com/gh/timwedde/rich-utils.svg?style=svg)](https://circleci.com/gh/timwedde/rich-utils)\n[![Downloads](https://pepy.tech/badge/rich-utils)](https://pepy.tech/project/rich-utils)\n\nUtility methods and classes for the "rich" package.\n',
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
