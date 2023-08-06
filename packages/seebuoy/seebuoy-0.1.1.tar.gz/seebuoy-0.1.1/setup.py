# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seebuoy', 'seebuoy._ndbc', 'seebuoy.ww3']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'pandas>=1.1.2,<2.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'seebuoy',
    'version': '0.1.1',
    'description': 'Remote data access for oceanographic data.',
    'long_description': None,
    'author': 'nickc1',
    'author_email': 'nickcortale@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
