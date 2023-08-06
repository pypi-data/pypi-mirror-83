# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ke2daira']

package_data = \
{'': ['*']}

install_requires = \
['Janome>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'ke2daira',
    'version': '0.1.2',
    'description': 'A Python implementaion of ke2daira',
    'long_description': '# ke2daira.py\n\nA Python implementation of [ke2daira](https://github.com/ryuichiueda/ke2daira)\n\n## Installation\n\n```\n$ pip install ke2daira\n```\n\n## Usage\n\n```py\nfrom ke2daira import ke2dairanize\n\nprint(ke2dairanize("松平 健")) # "ケツダイラ マン"\n```\n\n## Development\n\nInstall dependencies with poetry: `poetry install` \\\nRun type check: `poetry run mypy .` \\\nRun tests: `poetry run pytest` \\\nFormat code: `poetry run black .`\n\n\n## Difference from original ke2daira\n\n`ke2daira.py` only supports switching the head of the first word and the one of the last word.\n\n## License\n\nApache-2.0',
    'author': 'otariidae',
    'author_email': 'otariidae@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/otariidae/ke2daira.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
