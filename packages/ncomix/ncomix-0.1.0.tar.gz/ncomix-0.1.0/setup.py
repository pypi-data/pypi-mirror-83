# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ncomix']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=4.14.0,<5.0.0',
 'Pillow>=8.0.1,<9.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'ncomix',
    'version': '0.1.0',
    'description': "Simple module to download comics from 'https://www.porncomix.one' using webscrapping.",
    'long_description': '# ncomix version 0.1.0\n\nThis is a simple module to download comics from "https://www.porncomix.one" using webscrapping. \n\nThis version is the first prototype, more documentation and functionalities will be added soon\n\n## Basic Usage\n\nfrom ncomix import ncomix\n\ncomic = ncomix(url_to_comic)\n\ncomic.download() #download pages as images to a folder in current working directory\n\ncomic.download_pdf() #download combine pages to single pdf in current working directory\n\nTo download to given directory\n\ncomic.download(dest=mydir) #download to given directory\n\ncomic.download_pdf(dest=mydir)\n\nTo get basic info on the comic\n\nprint(comix)',
    'author': 'Beanco Mix',
    'author_email': 'dev.ncomix@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Beanco-Mix/ncomix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
