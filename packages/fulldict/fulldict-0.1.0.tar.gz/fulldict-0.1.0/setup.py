# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['fulldict']
setup_kwargs = {
    'name': 'fulldict',
    'version': '0.1.0',
    'description': 'Dictionaries with multiple functionalities.',
    'long_description': '# Full Dict\n\nLibrary that provides dictionaries with multiple functionalities.\n',
    'author': 'Eduardo Rezende',
    'author_email': 'eduardorbr7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/revensky/fulldict',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
