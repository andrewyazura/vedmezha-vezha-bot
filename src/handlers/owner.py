from telegram.ext import CallbackQueryHandler

from src import current_bot


@current_bot.register_handler(CallbackQueryHandler)
def button(update, context):
    query = update.callback_query
    command, args = query.data.split(":", maxsplit=1)

    if command == "remove":
        print(args)

    query.answer()
