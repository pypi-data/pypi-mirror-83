import logging

from django.conf import settings


class ConfigurationError(Exception):
    pass


SETTINGS = {}


def get_setting(attribute, default=None):
    if attribute in SETTINGS:
        return SETTINGS[attribute]

    SETTINGS[attribute] = getattr(settings, attribute, default)
    return SETTINGS[attribute]


####################################################
# db-logging
####################################################

def store_django_log_exceptions():
    return get_setting("STORE_DJANGO_LOG_EXCEPTIONS")


def store_logged_exception():
    default = False
    if not settings.DEBUG:
        default = True
    return get_setting("STORE_LOGGED_EXCEPTIONS", default)

####################################################
# logging
####################################################


def add_builtins():
    return get_setting("ADD_BUILTINS", True)


def log_dir():
    return get_setting("LOG_DIR", fail_log_path())


def log_format():
    return get_setting("LOG_FORMAT", "%(asctime)s %(levelname)s %(message)s")


def log_date_format():
    return get_setting("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")


def log_to_stdout():
    return get_setting("LOG_TO_STDOUT", True)


def log_sql():
    return get_setting("LOG_SQL", False)


def log_level():
    level = get_setting("LOG_LEVEL", "INFO")
    try:
        logging._checkLevel(level)
    except ValueError:
        raise ConfigurationError("LOG_LEVEL: %s is not a valid log level. Valid levels are: %s"
                                        % (level, logging._levelToName))
    return level


####################################################
# templates
####################################################

def base_template():
    base_template = get_setting("BASE_TEMPLATE")
    if not base_template:
        raise ConfigurationError("BASE_TEMPLATE must be defined in settings.")
    return base_template

####################################################
# misc-ish
####################################################


def print_at_startup():
    return get_setting("PRINT_AT_STARTUP", True)


def fail_log_path():
    return "/dev/null"
