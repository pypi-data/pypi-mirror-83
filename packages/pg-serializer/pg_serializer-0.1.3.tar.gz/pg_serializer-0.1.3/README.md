# pg_serializer: Very fast JSON serializer using Django and PostgreSQL

[![PyPI version](https://badge.fury.io/py/pg-serializer.svg)](https://pypi.org/project/pg-serializer/)
[![Python Version](https://img.shields.io/badge/python-3.8-blue.svg)](https://docs.python.org/3/whatsnew/3.8.html)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pipeline status](https://gitlab.com/kozlek/pg_serializer/badges/master/pipeline.svg)](https://gitlab.com/kozlek/pg_serializer/-/commits/master)
[![coverage report](https://gitlab.com/kozlek/pg_serializer/badges/master/coverage.svg)](https://gitlab.com/kozlek/pg_serializer/-/commits/master)

## Overview 

> Django REST framework is a powerful and flexible toolkit for building Web APIs.

Django Rest Framework is a great framework for building REST APIs on top of Django and 
it fits 99% of use cases.  
However, JSON serialization is done in Python and it can be very slow for 
some `list` endpoints that return a lot of records.

`pg_serializer` aims to soften this 1% issue by providing a way to do JSON serialization 
inside your PostgreSQL database. Indeed, PostgreSQL has a built-in support for JSON 
since version 9.2, and it is far more faster than Python's one. 

## Installation

```bash
pip install pg-serializer
```

## Basic usage

`pg_serializer` features an automatic `ModelSerializer` like DRF.

```python
from django.contrib.auth.models import User

import pg_serializer


class UserSerializer(pg_serializer.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "date_joined",
        )


json_str = UserSerializer(User.objects.all()).json
```

It also has preliminary support for ForeignKey relation using the Django `__` separator.

```python
import pg_serializer


class OrderSerializer(pg_serializer.ModelSerializer):
    buyer = pg_serializer.StringField(source="buyer__username")

    class Meta:
        model = Order
        fields = (
            "transaction_id",
            "transaction_time",
            "buyer",
            "is_gift",
            "shipping_date",
            "additional_data",
        )


json_str = OrderSerializer(Order.objects.all()).json
```

Full examples are available inside `tests/models.py` and `tests/serializers.py`.


## Disclaimer ⚠️

- `pg_serializer` is not designed to replace DRF serializers, only to speed up 
some endpoints when performance is becoming an issue
- `pg_serializer` is still in alpha development: bugs can occur and 
it doesn't support all Django fields and relations

## Roadmap

- reinforce the test suite
- implement (and document) custom datetime and decimal formatting
- document how to create custom serializer fields
- full support for ArrayField and JSONField
- complex queryset operations (GROUP BY, ...) support
