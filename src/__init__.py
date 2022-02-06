from logging.config import dictConfig

from tinydb import TinyDB

from config import Config
from src.telegram_bot import TelegramBot

current_bot = TelegramBot()


def create_app(config=Config):
    dictConfig(config.LOG_CONFIG)
    db = TinyDB(Config.DATABASE["FILE"])

    current_bot.init_bot(config)
    current_bot.init_db(db)

    import src.handlers  # noqa: F401

    return current_bot
