# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hydride']

package_data = \
{'': ['*']}

install_requires = \
['biotite>=0.22']

setup_kwargs = {
    'name': 'hydride',
    'version': '0.1.0',
    'description': 'Adding hydrogen atoms to molecular models',
    'long_description': 'Hydride\n=======\n\nAdding hydrogen atoms to molecular models\n',
    'author': 'Patrick Kunzmann',
    'author_email': 'patrick.kunzm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hydride.biotite-python.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
