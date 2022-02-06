from telegram import ParseMode
from telegram.ext import CallbackQueryHandler
from tinydb import Query

from src import current_bot


@current_bot.register_handler(CallbackQueryHandler)
@current_bot.log_update
@current_bot.protected
def button(update, context):
    query = update.callback_query
    query.answer()

    command, args = query.data.split(":", maxsplit=1)

    if command == "remove":
        current_bot.reservations.remove(Query().id == args)
        query.edit_message_text(
            query.message.text + "\nВидалено", parse_mode=ParseMode.HTML
        )
