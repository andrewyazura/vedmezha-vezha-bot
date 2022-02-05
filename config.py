from environs import Env

env = Env()
env.read_env()


class Config:
    BOT_TOKEN = env.str("BOT_TOKEN")

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
