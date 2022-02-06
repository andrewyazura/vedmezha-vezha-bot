from telegram.ext import CallbackQueryHandler

from src import current_bot, helpers


@current_bot.register_handler(CallbackQueryHandler)
def button(update, context):
    query = update.callback_query
    command, args = query.data.split(":", maxsplit=1)

    if command == "remove":
        helpers.delete_reservation(context.bot_data, args)

    query.answer()
