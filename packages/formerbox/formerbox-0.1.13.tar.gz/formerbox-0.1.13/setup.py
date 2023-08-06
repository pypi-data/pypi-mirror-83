# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formerbox',
 'formerbox.cli',
 'formerbox.cli.functional',
 'formerbox.common',
 'formerbox.contrib',
 'formerbox.data',
 'formerbox.data.samplers',
 'formerbox.models',
 'formerbox.modules',
 'formerbox.modules.callbacks',
 'formerbox.modules.metrics',
 'formerbox.optim',
 'formerbox.tasks',
 'formerbox.tasks.code',
 'formerbox.training',
 'formerbox.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'boto3>=1.15.11,<2.0.0',
 'datasets>=1.1.2,<2.0.0',
 'jsonlines>=1.2.0,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'more-itertools>=8.5.0,<9.0.0',
 'numpy>=1.19.2,<2.0.0',
 'overrides>=3.1.0,<4.0.0',
 'pandas>=1.0.4,<2.0.0',
 'pydriller>=1.15.2,<2.0.0',
 'pytorch-lightning>=1.0.2,<2.0.0',
 'sacrebleu>=1.4.13,<2.0.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'scipy>=1.4.1,<2.0.0',
 'spacy>=2.2.4,<3.0.0',
 'torch>=1.6.0,<2.0.0',
 'tqdm>=4.46.1,<5.0.0',
 'traitlets>=4.3.3,<5.0.0',
 'transformers>=3.4.0,<4.0.0',
 'tree_sitter>=0.1.1,<0.2.0',
 'typing_extensions>=3.7.4,<4.0.0',
 'typing_inspect>=0.6.0,<0.7.0',
 'wandb>=0.10.5,<0.11.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['formerbox-cli = formerbox.__main__:run_main']}

setup_kwargs = {
    'name': 'formerbox',
    'version': '0.1.13',
    'description': '',
    'long_description': None,
    'author': 'mozharovsky',
    'author_email': 'mozharovsky@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
