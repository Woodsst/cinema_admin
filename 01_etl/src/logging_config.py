import logging
from logging import config


def logger_config():
    log_config = {
        "version": 1,
        "root": {
            "handlers": ["console", "file"],
            "level": "DEBUG"
        },
        "handlers": {
            "file": {
                "formatter": "std_out",
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "filename": "all_messages.log"
            },
            "console": {
                "formatter": "std_out",
                "class": "logging.StreamHandler",
                "level": 'WARNING'
            }
        },
        "formatters": {
            "std_out": {
                "format": "%(asctime)s %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%d-%m-%Y %I:%M:%S"
            }
        },
    }

    config.dictConfig(log_config)


logger_config()
logger = logging.getLogger(__name__)
