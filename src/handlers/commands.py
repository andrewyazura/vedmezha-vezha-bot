from telegram.ext import CommandHandler

from src import current_bot


@current_bot.register_handler(CommandHandler, "start")
@current_bot.log_update_and_response
def start(update, context):
    user = update.effective_user
    return update.message.reply_text(rf"Hi {user.mention_markdown_v2()}\!")
