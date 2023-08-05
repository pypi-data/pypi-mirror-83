# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pg_serializer']

package_data = \
{'': ['*']}

install_requires = \
['django', 'djangorestframework', 'psycopg2']

setup_kwargs = {
    'name': 'pg-serializer',
    'version': '0.1.3',
    'description': 'Fast serializers for Django using Postgres database',
    'long_description': '# pg_serializer: Very fast JSON serializer using Django and PostgreSQL\n\n[![PyPI version](https://badge.fury.io/py/pg-serializer.svg)](https://pypi.org/project/pg-serializer/)\n[![Python Version](https://img.shields.io/badge/python-3.8-blue.svg)](https://docs.python.org/3/whatsnew/3.8.html)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pipeline status](https://gitlab.com/kozlek/pg_serializer/badges/master/pipeline.svg)](https://gitlab.com/kozlek/pg_serializer/-/commits/master)\n[![coverage report](https://gitlab.com/kozlek/pg_serializer/badges/master/coverage.svg)](https://gitlab.com/kozlek/pg_serializer/-/commits/master)\n\n## Overview \n\n> Django REST framework is a powerful and flexible toolkit for building Web APIs.\n\nDjango Rest Framework is a great framework for building REST APIs on top of Django and \nit fits 99% of use cases.  \nHowever, JSON serialization is done in Python and it can be very slow for \nsome `list` endpoints that return a lot of records.\n\n`pg_serializer` aims to soften this 1% issue by providing a way to do JSON serialization \ninside your PostgreSQL database. Indeed, PostgreSQL has a built-in support for JSON \nsince version 9.2, and it is far more faster than Python\'s one. \n\n## Installation\n\n```bash\npip install pg-serializer\n```\n\n## Basic usage\n\n`pg_serializer` features an automatic `ModelSerializer` like DRF.\n\n```python\nfrom django.contrib.auth.models import User\n\nimport pg_serializer\n\n\nclass UserSerializer(pg_serializer.ModelSerializer):\n    class Meta:\n        model = User\n        fields = (\n            "id",\n            "username",\n            "email",\n            "first_name",\n            "last_name",\n            "is_staff",\n            "date_joined",\n        )\n\n\njson_str = UserSerializer(User.objects.all()).json\n```\n\nIt also has preliminary support for ForeignKey relation using the Django `__` separator.\n\n```python\nimport pg_serializer\n\n\nclass OrderSerializer(pg_serializer.ModelSerializer):\n    buyer = pg_serializer.StringField(source="buyer__username")\n\n    class Meta:\n        model = Order\n        fields = (\n            "transaction_id",\n            "transaction_time",\n            "buyer",\n            "is_gift",\n            "shipping_date",\n            "additional_data",\n        )\n\n\njson_str = OrderSerializer(Order.objects.all()).json\n```\n\nFull examples are available inside `tests/models.py` and `tests/serializers.py`.\n\n\n## Disclaimer ⚠️\n\n- `pg_serializer` is not designed to replace DRF serializers, only to speed up \nsome endpoints when performance is becoming an issue\n- `pg_serializer` is still in alpha development: bugs can occur and \nit doesn\'t support all Django fields and relations\n\n## Roadmap\n\n- reinforce the test suite\n- implement (and document) custom datetime and decimal formatting\n- document how to create custom serializer fields\n- full support for ArrayField and JSONField\n- complex queryset operations (GROUP BY, ...) support\n',
    'author': 'Thomas Berdy',
    'author_email': 'thomas.berdy@outlook.com',
    'maintainer': 'Thomas Berdy',
    'maintainer_email': 'thomas.berdy@outlook.com',
    'url': 'https://gitlab.com/kozlek/pg_serializer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
