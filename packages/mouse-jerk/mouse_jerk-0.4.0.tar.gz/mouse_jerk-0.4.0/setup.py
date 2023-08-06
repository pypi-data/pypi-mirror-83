# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mouse_jerk']

package_data = \
{'': ['*']}

install_requires = \
['pynput>=1.7.1,<2.0.0']

entry_points = \
{'console_scripts': ['mouse_jerk = mouse_jerk.script:main']}

setup_kwargs = {
    'name': 'mouse-jerk',
    'version': '0.4.0',
    'description': 'Small app, that help your PC to not fall asleep.',
    'long_description': None,
    'author': 'd.finko',
    'author_email': 'dmit.finn@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gstr169/mouse_jerk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
