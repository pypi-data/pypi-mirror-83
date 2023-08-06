# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google-stubs']

package_data = \
{'': ['*'],
 'google-stubs': ['api/*',
                  'logging/*',
                  'logging/type/*',
                  'longrunning/*',
                  'rpc/*',
                  'rpc/context/*',
                  'type/*']}

install_requires = \
['googleapis-common-protos>=1.52.0,<2.0.0', 'typing-extensions>=3.7,<4.0']

extras_require = \
{':python_version < "3.5"': ['typing>=3.7,<4.0']}

setup_kwargs = {
    'name': 'googleapis-common-protos-stubs',
    'version': '1.1.1.post1',
    'description': 'Type stubs for googleapis-common-protos',
    'long_description': '# Type stubs for googleapis-common-protos\n[![PyPI version](https://badge.fury.io/py/googleapis-common-protos-stubs.svg)](https://badge.fury.io/py/googleapis-common-protos-stubs)\n\nThis package provides type stubs for the [googleapis-common-protos](https://pypi.org/project/googleapis-common-protos/) package.\n\n**This is in no way affiliated with Google.**\n\nThe stubs were created automatically by [mypy-protobuf](https://github.com/dropbox/mypy-protobuf).\n\n## Installation\n```shell script\n$ pip install googleapis-common-protos-stubs\n```\n',
    'author': 'Henrik Bruåsdal',
    'author_email': 'henrik.bruasdal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/henribru/googleapis-common-protos-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
