# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['retclient']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'reelib>=1.4.1,<2.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'retclient',
    'version': '0.1.5',
    'description': 'A client package for RetinaFace.',
    'long_description': '# retina_client',
    'author': 'reeve0930',
    'author_email': 'reeve0930@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reeve0930/pyzaim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
