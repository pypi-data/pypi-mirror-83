from django.conf import settings
from django.test.signals import setting_changed

from rest_framework.settings import APISettings as DrfAPISettings

DJANGO_SETTINGS_KEY = "PG_SERIALIZER"

DEFAULTS = {
    "COERCE_DECIMAL_TO_STRING": True,
    "JSON_AS_BYTES": False,
}


# List of settings that may be in string import notation.
IMPORT_STRINGS = ()


# List of settings that have been removed
REMOVED_SETTINGS = ()


class APISettings(DrfAPISettings):
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, DJANGO_SETTINGS_KEY, {})
        return self._user_settings

    def __check_user_settings(self, user_settings):
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    f"The '{setting}' setting has been removed. "
                    "Please refer to the documentation for available settings."
                )
        return user_settings


api_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == DJANGO_SETTINGS_KEY:
        api_settings.reload()


setting_changed.connect(reload_api_settings)
