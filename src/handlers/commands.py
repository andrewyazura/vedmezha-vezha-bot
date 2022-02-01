from telegram.ext import CommandHandler

from src import current_bot


@current_bot.register_handler(CommandHandler, "start")
def start(update, context) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(rf"Hi {user.mention_markdown_v2()}\!")
