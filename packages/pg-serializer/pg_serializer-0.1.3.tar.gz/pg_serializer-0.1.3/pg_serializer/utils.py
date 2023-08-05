from contextlib import contextmanager
from functools import reduce
from typing import List, Dict, Tuple

import psycopg2.extensions
from django.db import connection, models


def dict_merge(*dicts: List[Dict]) -> Dict:
    return reduce(lambda acc, d: {**acc, **(d or {})}, dicts, {})


def generate_custom_select_with_params(
    queryset: models.QuerySet, annotations: Dict[str, models.Expression]
) -> Tuple[str, Tuple]:
    """Force Django to generate a custom select statement.
    Using internal query API:
    1) clear out all the default queryset fields, and remove added annotations
    2) recreate the internal annotations register using the provided ones
    3) generate sql + params to escape. params will be escaped by psycopg2 later.

    Parameters
    ----------
    queryset: models.QuerySet
    annotations: Dict[str, models.Expression]

    Returns
    -------
    Tuple[str, Tuple]

    """
    queryset.query.default_cols = False
    queryset.query.annotations = {}

    for alias, annotation in annotations.items():
        queryset.query.add_annotation(annotation, alias, is_summary=False)

    return queryset.query.sql_with_params()


@contextmanager
def db_str_as_bytes():
    try:
        psycopg2.extensions.register_type(
            psycopg2.extensions.BYTES, connection.connection
        )
        psycopg2.extensions.register_type(
            psycopg2.extensions.BYTESARRAY, connection.connection
        )
        yield
    finally:
        psycopg2.extensions.register_type(
            psycopg2.extensions.UNICODE, connection.connection
        )
        psycopg2.extensions.register_type(
            psycopg2.extensions.UNICODEARRAY, connection.connection
        )
