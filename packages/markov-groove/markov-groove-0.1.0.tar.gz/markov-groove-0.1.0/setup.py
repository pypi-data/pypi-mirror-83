# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markov_groove', 'markov_groove.sequencer']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'essentia>=2.1b5,<3.0',
 'matplotlib>=3.1.3,<4.0.0',
 'more-itertools>=8.2.0,<9.0.0',
 'nptyping>=1.3.0,<2.0.0',
 'numpy==1.18.2',
 'pomegranate>=0.13.4,<0.14.0',
 'pretty_midi>=0.2.9,<0.3.0',
 'pyfluidsynth>=1.2.5,<2.0.0']

setup_kwargs = {
    'name': 'markov-groove',
    'version': '0.1.0',
    'description': 'Generate drum loops by using hidden markov chains.',
    'long_description': None,
    'author': 'Jan-Niclas de Vries',
    'author_email': 'jan_dev@uni-bremen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
