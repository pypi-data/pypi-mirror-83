# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_validated_jsonfield']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2.0',
 'djangorestframework>=3.11.0',
 'drf_yasg',
 'jsonschema',
 'jsonschema-to-openapi>=0.2.1']

setup_kwargs = {
    'name': 'django-validated-jsonfield',
    'version': '1.0.0',
    'description': 'Add a schema with validation to your jsonfield',
    'long_description': None,
    'author': 'Loic Quertenmont',
    'author_email': 'loic@youmeal.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
