# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['obschart', 'obschart.api', 'obschart.api.nodes', 'obschart.gql']

package_data = \
{'': ['*']}

install_requires = \
['graphql-core>=3.0.3,<4.0.0', 'httpx>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'obschart',
    'version': '1.2.0',
    'description': '',
    'long_description': None,
    'author': 'ObsChart',
    'author_email': 'contact@obschart.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
