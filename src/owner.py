from src import current_bot, keyboards


def send_reservation(reservation):
    message = (
        "*Нове замовлення*:\n"
        f"{reservation['table']}\n"
        f"{reservation['service_package']}\n"
        f"Дата: _{reservation['date']}_\n"
        f"Час: _{reservation['time']}_\n"
        f"Телефон: _{reservation['phone']}_\n"
        f"Ігри: _{reservation.get('board_games') or 'не вказано'}_\n"
    )

    current_bot.bot.send_message(
        chat_id=current_bot.config.BOT["OWNER_ID"],
        text=message.replace("-", r"\-"),
        reply_markup=keyboards.owner_commands(reservation["id"]),
    )
