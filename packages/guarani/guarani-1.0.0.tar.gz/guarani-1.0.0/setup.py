# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['guarani',
 'guarani.authentication',
 'guarani.authentication.methods',
 'guarani.endpoints',
 'guarani.grants',
 'guarani.mixins',
 'guarani.models',
 'guarani.providers']

package_data = \
{'': ['*']}

install_requires = \
['shiro>=0.2.2,<0.3.0']

setup_kwargs = {
    'name': 'guarani',
    'version': '1.0.0',
    'description': 'Asynchronous Authorization, Authentication and Identity Provider for Python using OAuth 2.1 and OpenID Connect.',
    'long_description': '# Project Guarani\n\nThis library provides an implementation for asynchronous\nauthentication and authorization of web applications.\nIt provides support for OAuth 2.1 and OpenID Connect.\n\nFor more details, please visit the documentation.\n\nAny doubts and suggestions can be sent to my [email](mailto:eduardorbr7@gmail.com).\nJust prepend the title with `#Guarani#`, and I will try my best to answer.\n\n## Supported Protocols and RFCs\n\n-   OAuth 2.1\n\n    -   [OAuth 2.1 Draft](https://tools.ietf.org/html/draft-parecki-oauth-v2-1)\n    -   [RFC 7009: Token Revocation](https://tools.ietf.org/html/rfc7009)\n\n-   OpenID Connect\n    -   [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)\n\n# License\n\nThis project is licensed under the MIT License.\nFor more details, please refer to the `LICENSE` file.\n',
    'author': 'Eduardo Rezende',
    'author_email': 'eduardorbr7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/revensky/guarani',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
