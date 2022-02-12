import logging

from src import current_bot, keyboards


def send_reservation(reservation, new=True):
    logger = logging.getLogger("telegram_bot")
    logger.debug(f"Sending reservation to owner: {reservation}")

    message = (
        f"{reservation['name']}\n"
        f"{reservation['table']}\n"
        f"{reservation['service_package']}\n"
        f"Дата: <i>{reservation['date']}</i>\n"
        f"Час: <i>{reservation['time']}</i>\n"
        f"Телефон: <i>{reservation['phone']}</i>\n"
        f"Кількість людей: <i>{reservation['amount']}</i>\n"
        f"Ігри: <i>{reservation.get('board_games') or 'не вказано'}</i>\n"
    )

    if new:
        message = "<b>Нове замовлення</b>:\n" + message

    message = current_bot.bot.send_message(
        chat_id=current_bot.config.BOT["OWNER_ID"],
        text=message,
        reply_markup=keyboards.owner_commands(reservation["id"]),
    )

    logger.debug(f"Sent reservation to owner: {message}")
