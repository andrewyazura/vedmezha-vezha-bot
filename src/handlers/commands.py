from telegram.ext import CommandHandler

from src import current_bot, keyboards


@current_bot.register_handler(CommandHandler, "start")
@current_bot.log_update
def start(update, context):
    user = update.effective_user
    user.send_message("Привіт! Я помічник клубу настільних ігор Ведмежа Вежа! 😉")
    user.send_message("Оберіть, що вас цікавить", reply_markup=keyboards.main_menu())
