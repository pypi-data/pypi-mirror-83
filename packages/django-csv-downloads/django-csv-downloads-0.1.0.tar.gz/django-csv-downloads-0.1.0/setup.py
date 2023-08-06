# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_csv', 'django_csv.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-csv-downloads',
    'version': '0.1.0',
    'description': 'Django app for tracking queryset-backed CSV downloads',
    'long_description': '# Django CSV Downloads\n\nDjango app for tracking queryset-backed CSV downloads\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-csv-downloads',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
