from config import Config
from src.telegram_bot import TelegramBot

current_bot = TelegramBot()


def create_app(config=Config):
    current_bot.init_bot(config)

    import src.handlers

    return current_bot
