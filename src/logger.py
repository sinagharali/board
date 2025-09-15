import json
import logging
from logging.config import dictConfig

# from config import settings


# Custom JSON Formatter based on Better Stack website
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)


LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": JsonFormatter,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "default": {
            "format": "%(asctime)s | %(levelname)s | %(module)s.%(funcName)s:%(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
            "level": "DEBUG",
        },
        "rotating_file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default",
            "level": "DEBUG",
        },
        # "logtail": {
        #     "class": "logtail.LogtailHandler",
        #     "level": "INFO",
        #     "source_token": settings.log_token,
        #     "host": settings.log_host,
        # },
    },
    "loggers": {
        "app": {
            "handlers": ["console", "rotating_file"],  # , "logtail"
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "rotating_file"],  # "logtail"
        "level": "DEBUG",
    },
}

dictConfig(LOG_CONFIG)
logger = logging.getLogger("app")
