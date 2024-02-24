import os
from dotenv import load_dotenv
from logging.config import dictConfig
import logging

load_dotenv()

TOKEN = os.getenv("TOKEN")


LOGGING_CONFIG = {
    "version" : 1,
    "disabled_existing_loggers" : False,
    "formatters" : {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level" : "DEBUG",
            "class" : "logging.StreamHandler",
            "formatter" : "standard"
        },
        "console2": {
            "level" : "WARNING",
            "class" : "logging.StreamHandler",
            "formatter" : "standard"
        },
        "file": {
            "level" : "DEBUG",
            "class" : "logging.FileHandler",
            "filename" : "logs/infos.log",
            "mode" : "w",
            "formatter" : "verbose"
        }
    },
    "Loggers" : {
        "bot" : {
            'handlers' : ["console", "file"],
            'level' : "DEBUG",
            'propagate' : False
        },
        "discord" : {
            'handlers' : ["console2", "file"],
            'level' : "INFO",
            'propagate' : False
        },
    },
}


dictConfig(LOGGING_CONFIG)
