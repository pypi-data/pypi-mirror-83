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
    'version': '1.0.1',
    'description': 'Add a schema with validation to your jsonfield',
    'long_description': "# django_validated_jsonfield\n\ndjango_validated_jsonfield is an inplace replacement for JSONField which supports providing a json_schema for validating the field's data via django validation and also via rest framework serializer fields.\nThe field is also documented using drf_yasg",
    'author': 'Loic Quertenmont',
    'author_email': 'loic@youmeal.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/loic.quertenmont/django_validated_jsonfield',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
