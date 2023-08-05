from django.db import models


class ToChar(models.Func):
    function = "TO_CHAR"
    output_field = models.TextField()
    text_format = None

    def __init__(self, expression: models.Expression, text_format: str = None, **extra):
        super().__init__(
            expression, models.Value(text_format or self.text_format), **extra,
        )


class ToIsoDate(ToChar):
    text_format = "YYYY-MM-DD"


class ToIsoDateTime(ToChar):
    text_format = 'YYYY-MM-DD"T"HH24:MI:SS.USTZH:TZM'
