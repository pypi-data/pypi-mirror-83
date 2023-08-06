# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['scrapedict']
install_requires = \
['beautifulsoup4>=4.9,<5.0', 'parse>=1.18,<2.0']

setup_kwargs = {
    'name': 'scrapedict',
    'version': '0.1.1',
    'description': 'Scrape HTML to dictionaries',
    'long_description': None,
    'author': 'Pedro Rodrigues',
    'author_email': 'medecau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/medecau/scrapedict',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
