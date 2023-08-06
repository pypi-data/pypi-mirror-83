# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poshpy', 'tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poshpy',
    'version': '0.1.0',
    'description': 'Top-level package for poshpy.',
    'long_description': '======\nposhpy\n======\n\n\n.. image:: https://img.shields.io/pypi/v/poshpy.svg\n        :target: https://pypi.python.org/pypi/poshpy\n\n.. image:: https://github.com/BlueGhostLabs/poshpy/workflows/Tests/badge.svg?branch=main\n        :target: https://github.com/BlueGhostLabs/poshpy/actions?query=workflow%3ATests\n\n.. image:: https://readthedocs.org/projects/poshpy/badge/?version=latest\n        :target: https://poshpy.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\nA Python package for working with PowerShell.\n\n\n* Free software: Apache-2.0\n* Documentation: https://poshpy.readthedocs.io.\n\n\nFeatures\n--------\n\n* Ability to execute PowerShell with a Command, EncodedCommand, or File option using Python.\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Jamie Phillips',
    'author_email': 'jamie@blueghostlabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/blueghostlabs/poshpy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
