# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitscrum', 'gitscrum.utils']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1,<0.4.0',
 'termcolor>=1.1.0,<2.0.0',
 'terminaltables>=3.1.0,<4.0.0']

entry_points = \
{'console_scripts': ['gitscrum = gitscrum:main']}

setup_kwargs = {
    'name': 'gitscrum',
    'version': '0.0.1',
    'description': 'A CLI for scrum tasks with git',
    'long_description': '# gitscrum',
    'author': 'Conor Sheehan',
    'author_email': 'conor.sheehan.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ConorSheehan1/gitscrum',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
