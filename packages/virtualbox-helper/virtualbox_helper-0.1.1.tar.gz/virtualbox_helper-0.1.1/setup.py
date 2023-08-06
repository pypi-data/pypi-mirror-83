# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virtualbox_helper']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'remotevbox>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['main = virtualbox_helper.__main__:main',
                     'test = pytest:console_main']}

setup_kwargs = {
    'name': 'virtualbox-helper',
    'version': '0.1.1',
    'description': 'Start and control a virtualbox machine',
    'long_description': None,
    'author': 'Jacopo Farina',
    'author_email': 'jacopo1.farina@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
