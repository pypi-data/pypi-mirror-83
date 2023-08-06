# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_to_snowflake']

package_data = \
{'': ['*']}

install_requires = \
['snowflake-connector-python==2.2.10']

entry_points = \
{'console_scripts': ['csv-to-snowflake = csv_to_snowflake.main:run']}

setup_kwargs = {
    'name': 'csv-to-snowflake',
    'version': '0.2.1',
    'description': 'Creates a table in Snowflake based on CSV file',
    'long_description': None,
    'author': 'Dmitry Belov',
    'author_email': 'pik4ez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
