from colorama import Fore, Style
from django.conf import settings
from django.db import connection

from fandango.conf.settings import log_dir, log_level, store_logged_exception, store_django_log_exceptions, log_sql
from fandango.utils.models import get_editable_models

editable_models = get_editable_models()

print(Fore.LIGHTBLUE_EX + "*********************************************************************")
if getattr(settings, "DEBUG"):
    print(Fore.LIGHTYELLOW_EX + "We're running in " + Fore.MAGENTA + "debug")
else:
    print(Fore.LIGHTYELLOW_EX + "We're NOT running in " + Fore.LIGHTBLUE_EX + "debug")

print(Fore.LIGHTYELLOW_EX + "Database backend:\t" + connection.vendor)
print("Using database:\t\t" + connection.settings_dict['NAME'])
print("Log-dir:\t\t" + log_dir())
print("Log level:\t\t" + log_level())
print("Static root:\t\t" + getattr(settings, "STATIC_ROOT"))
print("Static url:\t\t" + getattr(settings, "STATIC_URL"))
print("Media root:\t\t" + getattr(settings, "MEDIA_ROOT"))
print("Media url:\t\t" + getattr(settings, "MEDIA_URL"))

if editable_models:
    print("Editable models:\t" + str(get_editable_models()))

if log_sql():
    print(Fore.GREEN + "* Logging SQL")

if store_logged_exception():
    print(Fore.GREEN + "* Storing internal log exceptions")

if store_django_log_exceptions():
    print(Fore.GREEN + "* Storing Django log exceptions")

print(Fore.LIGHTBLUE_EX + "*********************************************************************")
print(Style.RESET_ALL)
