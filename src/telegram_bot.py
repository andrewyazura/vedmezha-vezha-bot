import logging
from functools import wraps

from telegram.ext import Updater, Defaults


class TelegramBot:
    def __init__(self, config=None):
        if config:
            self.init_bot(config)

    def init_bot(self, config):
        self.config = config
        self.logger = logging.getLogger("telegram_bot")

        defaults = Defaults(**config.DEFAULTS)
        self.updater = Updater(config.BOT_TOKEN, defaults=defaults)
        self.dispatcher = self.updater.dispatcher

    def register_handler(self, handler_class, *args, **kwargs):
        def decorator(f):
            handler = handler_class(*args, **kwargs, callback=f)
            self.dispatcher.add_handler(handler)
            return f

        return decorator

    def log_update(self, f):
        @wraps(f)
        def decorated_function(update, context, *args, **kwargs):
            self.logger.debug(f"Update: {str(update)}")
            return f(update, context, *args, **kwargs)

        return decorated_function
