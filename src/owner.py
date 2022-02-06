from telegram import ParseMode

from src import current_bot, keyboards


def send_reservation(reservation):
    message = (
        "<b>Нове замовлення</b>:\n"
        f"{reservation['table']}\n"
        f"{reservation['service_package'].name}\n"
        f"Дата: <i>{reservation['date']}</i>\n"
        f"Час: <i>{reservation['time']}</i>\n"
        f"Телефон: <i>{reservation['phone']}</i>\n"
        f"Ігри: <i>{reservation.get('board_games') or 'не вказано'}</i>\n"
    )

    current_bot.bot.send_message(
        chat_id=current_bot.config.BOT["OWNER_ID"],
        text=message,
        reply_markup=keyboards.owner_commands(reservation["id"]),
        parse_mode=ParseMode.HTML,
    )
