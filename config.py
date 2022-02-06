from collections import namedtuple
from datetime import timedelta

from environs import Env

env = Env()
env.read_env(override=True)


class Config:
    with env.prefixed("BOT_"):
        BOT = {
            "TOKEN": env.str("TOKEN"),
            "OWNER_ID": env.int("OWNER_ID"),
            "REPORT_ID": env.int("REPORT_ID"),
        }

    with env.prefixed("DEFAULTS_"):
        DEFAULTS = {
            "parse_mode": env.str("PARSE_MODE"),
            "run_async": env.bool("RUN_ASYNC"),
        }

    with env.prefixed("LOG_"):
        LOG_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "file": {"format": env.str("FORMAT"), "datefmt": env.str("DATEFMT")}
            },
            "handlers": {
                "file": {
                    "level": env.log_level("LEVEL"),
                    "formatter": "file",
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": env.str("FILENAME"),
                    "when": "midnight",
                    "backupCount": env.int("BACKUP_COUNT"),
                    "utc": True,
                }
            },
            "loggers": {
                "telegram_bot": {"level": env.log_level("LEVEL"), "handlers": ["file"]}
            },
        }

    with env.prefixed("CLUB_"):
        CLUB = {
            "TABLES": env.int("TABLES"),
            "TABLE_FORMAT": env.str("TABLE_FORMAT"),
            "RESERVATION_TIMEDELTA": timedelta(
                **env.dict("RESERVATION_TIMEDELTA", subcast_values=int)
            ),
            "OPENING_TIME": timedelta(**env.dict("OPENING_TIME", subcast_values=int)),
            "CLOSING_TIME": timedelta(**env.dict("CLOSING_TIME", subcast_values=int)),
            "TIME_PERIOD": timedelta(**env.dict("TIME_PERIOD", subcast_values=int)),
        }

    SERVICE_PACKAGES = [
        {
            "name": "Бронювання на 1 годину",
            "price": 40,
            "timedelta": timedelta(hours=1),
        },
        {"name": "Безлім", "price": 100, "timedelta": timedelta(days=1)},
    ]

    with env.prefixed("FILE_URL_"):
        FILES = {"ABOUT": env.str("ABOUT"), "LOCATION": env.str("LOCATION")}

    with env.prefixed("DATABASE_"):
        DATABASE = {"FILE": env.str("FILE")}
