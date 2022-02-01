import logging
from logging.config import dictConfig

from telegram.ext import Updater


class TelegramBot:
    def __init__(self, config=None):
        if config:
            self.init_bot(config)

    def init_bot(self, config):
        self.config = config

        self.updater = Updater(config.BOT_TOKEN)
        self.dispatcher = self.updater.dispatcher

        self._init_logging()

    def _init_logging(self):
        dictConfig(self.config.LOG_CONFIG)
        self.logger = logging.getLogger("telegram_bot")

    def register_handler(self, handler_class, *args, **kwargs):
        def decorator(f):
            handler = handler_class(*args, **kwargs, callback=f)
            self.dispatcher.add_handler(handler)
            return f

        return decorator
