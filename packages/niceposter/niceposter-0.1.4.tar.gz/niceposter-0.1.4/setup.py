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
    'version': '0.1.4',
    'description': 'Image Manipulation Tool - Used for creating & modifying image posters',
    'long_description': '<p align="center">\n  <img src="https://raw.githubusercontent.com/amajai/niceposter/main/res/icon.png" width="180">\n<p>\n\n# Niceposter\nA library that allows you to create your own image poster which you can use to share on social media. Implemented in Python using the PIL module.\n\n<img src="https://raw.githubusercontent.com/amajai/niceposter/main/res/demo.gif">\n\n## **Installation**\n```elm\npip install niceposter\n```\n__Important:__ depending on your system, make sure to use `pip3` and `python3` instead.\n\n\n**That\'s all! 🎉**   \n\n>If you would like to install a specific version of Niceposter you may do so with:\n>```elm\n>pip install niceposter==0.1.1\n>```\n#### Using Niceposter\n\nTo start creating an image poster, you have to initialize it, like so: \n```python\nfrom niceposter import Create\n\nbg_image = Create.Poster() # default size of 500x500\n```\n\nThen use any one of the methods to make or add changes to an image. Examples:\n```python\nbg_image.add_image(\'cool-image.png\', position=\'cc\', scale=20) # added in center of the bg image and scaled down by 20%\nbg_image.text(\'Interesting text!\', position(50,50), color=\'red\', align=\'center\')\nbg_image.frame(thickness=10)\nbg_image.filter(rgb=(255,255,255), opacity=50)\n```\n\n#### Updating Niceposter\n```elm\npip install niceposter -U\n```\n## Documentation\n[**In progress**]\n\n## Features in progress\n[**In progress**]\n\n## Documentation\nContributions are welcome, and they are greatly appreciated! Every little bit\nhelps, and credit will always be given.\n\n\n',
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
