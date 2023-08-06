# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niceposter']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'niceposter',
    'version': '0.1.2',
    'description': 'Image Manipulation Tool - Used for creating & modifying image posters',
    'long_description': '<p align="center">\n  <img src="https://raw.githubusercontent.com/amajai/niceposter/main/res/icon.png" width="180">\n<p>\n\n# Niceposter\nA library that allows you to create your own image poster which you can use to share on social media. Implemented in Python using the PIL module.\n',
    'author': 'A.A.Isa',
    'author_email': 'aabdulmajeed.isa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
