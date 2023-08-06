from fandango.db.models.django_log_entry import DjangoLogEntry
from fandango.db.models.logged_exception import LoggedException
from fandango.utils.models import get_editable_models_dict


def globals(request):
    return {
        "EDITABLE_MODELS": get_editable_models_dict(),
        "UNHANDLED_LOGGED_EXCEPTIONS": LoggedException.unhandled.all(),
        "UNHANDLED_DJANGO_LOG_ENTRIES": DjangoLogEntry.unhandled.all(),
    }
