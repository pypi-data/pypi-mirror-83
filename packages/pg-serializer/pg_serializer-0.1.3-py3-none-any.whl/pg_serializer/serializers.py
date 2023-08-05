from operator import attrgetter
from typing import Any, Dict, Sequence, Set, Tuple, Type

from django.db import connection, models, ProgrammingError
from django.utils.functional import cached_property

from .fields import Field, get_json_field_class_from_django_field
from .settings import api_settings
from .utils import dict_merge, generate_custom_select_with_params, db_str_as_bytes


class SerializerMetaclass(type):
    @classmethod
    def _get_declared_fields_from_bases(cls, bases: Sequence) -> Dict[str, Field]:
        def _has_base_fields(base):
            return (
                isinstance(base, cls)
                and hasattr(base, "_meta")
                and hasattr(base._meta, "declared_fields")
            )

        bases_fields = [
            base._meta.fields for base in reversed(bases) if _has_base_fields(base=base)
        ]
        return dict_merge(*bases_fields)

    @classmethod
    def _get_declared_fields(
        cls,
        name: str,
        bases: Sequence,
        attrs: Dict[str, Any],
        meta_fields: Sequence[str],
    ) -> Dict[str, Field]:
        bases_fields = cls._get_declared_fields_from_bases(bases=bases)
        local_fields = {
            name: attrs.pop(name)
            for name, obj in list(attrs.items())
            if isinstance(obj, Field)
        }

        if any(field not in meta_fields for field in local_fields):
            raise ProgrammingError(
                f"[{name}] One or more declared fields are not present in Meta.fields"
            )
        return {**bases_fields, **local_fields}

    @classmethod
    def _generate_auto_fields(
        cls, model: Type[models.Model], field_names: Set[str]
    ) -> Dict[str, Field]:
        return {
            field_name: get_json_field_class_from_django_field(
                dj_field_class=model._meta.get_field(field_name=field_name).__class__
            )()
            for field_name in field_names
        }

    def __new__(cls, name, bases, attrs):
        if name == "ModelSerializer":
            return super().__new__(cls, name, bases, attrs)

        model, meta_fields = attrgetter("model", "fields")(attrs["Meta"])

        declared_fields = cls._get_declared_fields(
            name=name, bases=bases, attrs=attrs, meta_fields=meta_fields
        )
        auto_fields = cls._generate_auto_fields(
            model=model,
            field_names=set(meta_fields).difference(set(declared_fields.keys())),
        )
        all_fields = {**declared_fields, **auto_fields}
        fields = {field: all_fields[field] for field in meta_fields}

        kls = super().__new__(cls, name, bases, attrs)

        # bind fields to this serializer
        for field_name, field_obj in fields.items():
            field_obj.bind(field_name=field_name, serializer=kls)

        # add back useful attrs
        meta_attrs = {
            "model": model,
            "declared_fields": declared_fields,
            "fields": fields,
        }
        setattr(kls, "_meta", type("Meta", (), meta_attrs))

        return kls


class ModelSerializer(metaclass=SerializerMetaclass):
    def __init__(self, queryset: models.QuerySet, as_bytes: bool = None):
        self.queryset = queryset
        self.as_bytes = as_bytes if as_bytes is not None else api_settings.JSON_AS_BYTES

    @property
    def query_with_params(self) -> Tuple[str, Dict]:
        field_expressions = dict_merge(
            *[field.expression() for field in self._meta.fields.values()]
        )
        sql, params = generate_custom_select_with_params(
            queryset=self.queryset, annotations=field_expressions
        )

        query = f"""
        WITH query AS ({sql})
        SELECT ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(query)))::TEXT FROM query
        """
        return query, params

    def _run_query(self):
        with connection.cursor() as cursor:
            cursor.execute(*self.query_with_params)
            json_bytes = cursor.fetchone()[0]

        return json_bytes

    def to_representation(self) -> str or bytes:
        if self.as_bytes:
            with db_str_as_bytes():
                res = self._run_query()
        else:
            res = self._run_query()

        if res is None:
            res = b"[]" if self.as_bytes else "[]"

        return res

    @cached_property
    def json(self) -> str or bytes:
        return self.to_representation()
