# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['webtools']
install_requires = \
['fulldict>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'revensky.webtools',
    'version': '1.0.0',
    'description': 'Functionalities for easier web development.',
    'long_description': '# Project Web Tools\n\nThis library provides functionalities to assist web development.\n\n# License\n\nThis project is licensed under the MIT License.\nFor more details, please refer to the `LICENSE` file.\n',
    'author': 'Eduardo Rezende',
    'author_email': 'eduardorbr7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/revensky/webtools',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
