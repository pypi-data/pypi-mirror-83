# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bstadlbauer', 'bstadlbauer.p300speller']

package_data = \
{'': ['*'],
 'bstadlbauer.p300speller': ['conf_files/*',
                             'flash_images/*',
                             'number_images/*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0', 'numpy>=1.19.2,<2.0.0', 'pylsl>=1.13.6,<2.0.0']

entry_points = \
{'console_scripts': ['start-speller = '
                     'bstadlbauer.p300speller.p300_speller:main']}

setup_kwargs = {
    'name': 'bstadlbauer.p300speller',
    'version': '0.1.1',
    'description': 'P300 speller based on LSL',
    'long_description': "# LSL P300 speller\nThis repository contains a P300 speller based on [LSL](https://github.com/sccn/labstreaminglayer) and tkinter.\n\n## Installation\n\n### Dependencies\nThis project uses [poetry](https://python-poetry.org/) to manage its dependencies. Visit their website on how to install\npoetry for you operating system. The whole projects supports `python>=3.6.1`.\n\n### Installing the package\nRun the following to install the `bstadlbauer.p300speller` package:\n```\ngit clone https://github.org/bstadlbauer/lsl-p300-speller\npoetry install\n```\nwhich will setup a new virtual environment for the project and install the necessary dependencies.\n\n## Getting Started\nAfter installation, an entrypoint is avaibable to start the speller\n```\npoetry run start-speller\n```\n\n## Questions and Issues\nIf there are any questions or you run into an issue, please file a 'Issue' at the top.\n\n## Contributing\nIf you want to contribute, please file also file an issue first where the new feature can be discussed, in general\ncontribution is welcome!\n\nTo setup the development environment, do the following:\n```\ngit clone https://github.org/bstadlbauer/lsl-p300-speller\npoetry install\npre-commit install\n```\nTo ensure consistent formatting and linting pre-commit hooks (managed through [`pre-commit`](https://pre-commit.com/))\nare used.\n\n# Acknowledgement\nThis tool was developed by myself as part of a project done at the\n[Institute of Neural Engineering](https://www.tugraz.at/institutes/ine/home/).\nThe work was supervised by Assoc.Prof. Dipl.-Ing. Dr.techn. Reinhold Scherer.\n",
    'author': 'Bernhard Stadlbauer',
    'author_email': 'b.stadlbauer@gmx.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bstadlbauer/lsl-p300-speller',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
