from telegram.ext import Filters, MessageHandler

from src import current_bot


@current_bot.register_handler(MessageHandler, Filters.regex(r"^Про клуб 🙌$"))
@current_bot.log_update
def about(update, context):
    user = update.effective_user
    user.send_photo(photo=current_bot.config.FILES["ABOUT"])
    user.send_message(
        "Всім привіт! 🤩"
        "\n"
        "Раді вас вітати в найтеплішому й "
        "найцікавішому клубі настільних ігор 👋"
        "\n"
        "Дуже раді, що завітали до нас!"
    )


@current_bot.register_handler(MessageHandler, Filters.regex(r"^Контакти 📲$"))
@current_bot.log_update
def contacts(update, context):
    user = update.effective_user
    user.send_message(
        "<b>Адреса:</b> Бровари, вул. Киівська 245" "\n" "<b>Телефон:</b> 095 35 21 351"
    )


@current_bot.register_handler(MessageHandler, Filters.regex(r"^Місце розташування 🌍$"))
@current_bot.log_update
def location(update, context):
    user = update.effective_user
    user.send_photo(photo=current_bot.config.FILES["LOCATION"])
