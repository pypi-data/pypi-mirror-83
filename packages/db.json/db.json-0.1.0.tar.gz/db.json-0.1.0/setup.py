# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['db_json']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7,<2.0',
 'starlette>=0.13.8,<0.14.0',
 'typer>=0.3.2,<0.4.0',
 'uvicorn>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'db.json',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Andrii Maksymov',
    'author_email': 'maximov.echo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
