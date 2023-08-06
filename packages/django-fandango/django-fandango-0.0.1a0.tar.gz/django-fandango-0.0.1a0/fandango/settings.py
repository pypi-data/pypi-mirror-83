from fandango.conf.settings import log_format, log_date_format, log_dir, log_sql

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': log_format(),
            'datefmt': log_date_format(),
        }
    },
    'handlers': {
        'django': {
            'level': 'ERROR',
            'class': 'fandango.logging.handlers.DjangoLogHandler',
            'filename': log_dir() + 'django.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django'],
            'propagate': False,
            'level': 'DEBUG',
        },
    },
    'sql': {
        'level': 'DEBUG',
        'class': 'fandango.logging.handler.FileHandler',
        'filename': log_dir() + 'sql-shish.log',
        'formatter': 'verbose'
    },
}

if log_sql():
    LOGGING["loggers"]["django.db.backends"] = {
        'level': 'DEBUG', # always debug on this one
        'handlers': ['sql']
    }
