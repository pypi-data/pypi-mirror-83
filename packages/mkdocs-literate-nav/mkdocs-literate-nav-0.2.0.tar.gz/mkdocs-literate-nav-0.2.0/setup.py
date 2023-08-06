# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_literate_nav']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs>=1.0,<2.0']

entry_points = \
{'mkdocs.plugins': ['literate-nav = '
                    'mkdocs_literate_nav.plugin:LiterateNavPlugin']}

setup_kwargs = {
    'name': 'mkdocs-literate-nav',
    'version': '0.2.0',
    'description': 'MkDocs plugin to specify the navigation in Markdown instead of YAML',
    'long_description': None,
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oprypin/mkdocs-literate-nav',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
