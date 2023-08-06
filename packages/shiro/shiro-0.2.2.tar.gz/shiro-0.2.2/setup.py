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
['cryptography>=3.1.1,<4.0.0',
 'fulldict>=0.1.0,<0.2.0',
 'revensky.webtools>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'shiro',
    'version': '0.2.2',
    'description': 'JOSE implementation for Python.',
    'long_description': '# Python JSON Object Signing and Encryption (Project Shiro)\n\nThis library provides an implementation for the work of the JOSE Work Group.\n\nIt implements the following RFCs.\n\n1. [x] RFC 7515 - Json Web Signature (JWS)\n2. [ ] RFC 7516 - Json Web Encryption (JWE)\n3. [x] RFC 7517 - Json Web Key and Keyset (JWK)\n4. [x] RFC 7518 - Json Web Algorithms (JWA)\n5. [x] RFC 7519 - Json Web Token (JWT)\n\nFor more details on each feature, please visit the respective documentation.\n\n# License\n\nThis project is licensed under the MIT License.\n',
    'author': 'Eduardo Rezende',
    'author_email': 'eduardorbr7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/revensky/shiro',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
