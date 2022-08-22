import os

import git

repo = git.Repo(search_parent_directories=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app": {
            "format": (
                "%(asctime)s [%(levelname)-8s] (%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "logstash": {
            "()": "logstash_async.formatter.DjangoLogstashFormatter",
            "message_type": "django-logstash",
            "fqdn": False,
            # To disable grouping of the extra items and have them on the top level of the log event message, simply set this option to None or the empty string.
            "extra_prefix": None,
            "metadata": {"beat": "backend-api", "version": "1"},
            "extra": {
                "application": "backend-api",
                "version": repo.head.object.hexsha,
                "project_path": os.getcwd(),
                "environment": "production",
            },
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "app",
        },
        "logstash": {
            "level": "DEBUG",
            "class": "logstash_async.handler.AsynchronousLogstashHandler",
            "formatter": "logstash",
            "transport": "logstash_async.transport.TcpTransport",
            "host": "localhost",
            "port": 5959,
            "database_path": "{}/logstash.db".format(os.getcwd()),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "django.server": {
            "handlers": ["logstash"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
