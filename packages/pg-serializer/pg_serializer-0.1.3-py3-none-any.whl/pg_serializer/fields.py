from typing import Dict, Type

from django.contrib.postgres import fields as postgres_fields
from django.db.models import fields
from django.db.models.functions import Cast

from .expressions import ToIsoDate, ToIsoDateTime
from .settings import api_settings


class FieldMetaclass(type):
    def __new__(cls, name, bases, attrs):
        dj_fields = attrs.get("django_field_types", ())
        kls = super().__new__(cls, name, bases, attrs)
        kls._field_types_mapping.update({dj_field: kls for dj_field in dj_fields})
        return kls


# Abstract base field
class Field(metaclass=FieldMetaclass):
    _field_types_mapping = {}
    django_field_types = ()
    cast_type = None

    def __init__(self, source: str = None):
        self._source = source
        self.field_name = None
        self.serializer = None

    @property
    def source(self):
        return self._source or self.field_name

    def bind(self, field_name: str, serializer):
        self.field_name = field_name
        self.serializer = serializer

    def get_cast_type_params(self) -> Dict:
        return {}

    def expression(self):
        output_field = self.cast_type(**self.get_cast_type_params())
        return {self.field_name: Cast(self.source, output_field=output_field)}


# Base Json fields
class StringField(Field):
    django_field_types = (fields.CharField, fields.TextField, fields.UUIDField)
    cast_type = fields.TextField


class BooleanField(Field):
    django_field_types = (
        fields.BooleanField,
        fields.NullBooleanField,
    )
    cast_type = fields.BooleanField


class IntField(Field):
    django_field_types = (fields.IntegerField,)
    cast_type = fields.IntegerField


class BigIntField(IntField):
    django_field_types = (fields.BigIntegerField,)
    cast_type = fields.BigIntegerField


class FloatField(Field):
    django_field_types = (fields.FloatField,)
    cast_type = fields.FloatField


class DecimalField(Field):
    django_field_types = (fields.DecimalField,)
    cast_type = fields.DecimalField

    def __init__(self, coerce_to_string: bool = None, **kwargs):
        super().__init__(**kwargs)
        self.coerce_to_string = (
            coerce_to_string
            if coerce_to_string is not None
            else api_settings.COERCE_DECIMAL_TO_STRING
        )

    def get_cast_type_params(self) -> Dict:
        base_field = self.serializer._meta.model._meta.get_field(field_name=self.source)
        return {
            "max_digits": base_field.max_digits,
            "decimal_places": base_field.decimal_places,
        }

    def expression(self):
        if self.coerce_to_string:
            return {self.field_name: Cast(self.source, output_field=fields.TextField())}
        return super().expression()


class ObjectField(Field):
    django_field_types = (postgres_fields.JSONField,)
    cast_type = postgres_fields.JSONField


class ArrayField(Field):
    django_field_types = (postgres_fields.ArrayField,)
    cast_type = postgres_fields.ArrayField

    def get_cast_type_params(self) -> Dict:
        base_field = self.serializer._meta.model._meta.get_field(field_name=self.source)
        return {"base_field": base_field}


# Custom fields
class DateField(StringField):
    django_field_types = (fields.DateField,)
    cast_type = fields.TextField

    def expression(self):
        return {self.field_name: ToIsoDate(expression=self.source)}


class DateTimeField(StringField):
    django_field_types = (fields.DateTimeField,)
    cast_type = fields.TextField

    def expression(self):
        return {self.field_name: ToIsoDateTime(expression=self.source)}


def get_json_field_class_from_django_field(dj_field_class: Type[fields.Field]):
    # 1) try to get field class directly
    if json_field_class := Field._field_types_mapping.get(dj_field_class):
        return json_field_class

    # try to get a closest type
    for field_class, json_field in reversed(Field._field_types_mapping.items()):
        if issubclass(dj_field_class, field_class):
            return json_field

    raise ValueError(f"No JSON type is registered for {dj_field_class}.")
