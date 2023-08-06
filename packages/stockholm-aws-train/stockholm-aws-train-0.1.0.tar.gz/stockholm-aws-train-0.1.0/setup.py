# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stockholm_aws_train']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.2,<2.0.0', 'fabric>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'stockholm-aws-train',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Amresh Venugopal',
    'author_email': 'amresh.venugopal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
