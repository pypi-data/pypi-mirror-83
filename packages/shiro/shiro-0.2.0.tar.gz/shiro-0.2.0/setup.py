# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shiro',
 'shiro.jwa',
 'shiro.jwa.jwk',
 'shiro.jwa.jws',
 'shiro.jwk',
 'shiro.jws',
 'shiro.jwt']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.1.1,<4.0.0', 'fulldict>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'shiro',
    'version': '0.2.0',
    'description': 'JOSE implementation for Python.',
    'long_description': None,
    'author': 'Eduardo Rezende',
    'author_email': 'eduardorbr7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
