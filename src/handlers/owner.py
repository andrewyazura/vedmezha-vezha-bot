from telegram import ParseMode
from telegram.ext import CallbackQueryHandler, CommandHandler
from tinydb import Query

from src import current_bot, owner


@current_bot.register_handler(CommandHandler, "reservations")
@current_bot.log_update
@current_bot.protected
def get_reservations_list(update, context):
    reservations = current_bot.reservations.all()

    if not reservations:
        update.effective_user.send_message("Немає бронювань")

    for r in reservations:
        owner.send_reservation(r, new=False)


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
            query.message.text + "\n\n<b>Скасовано</b>", parse_mode=ParseMode.HTML
        )


@current_bot.register_handler(CommandHandler, "help")
@current_bot.log_update
@current_bot.protected
def help(update, context):
    user = update.effective_user
    user.send_message("/reservations - список бронювань")
