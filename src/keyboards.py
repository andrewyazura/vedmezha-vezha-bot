import datetime

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src import current_bot

club_config = current_bot.config.CLUB


def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["Про клуб 🙌", "Забронювати столик 🗓️"],
            ["Контакти 📲", "Місце розташування 🌍"],
        ],
        resize_keyboard=True,
    )


def tables():
    return ReplyKeyboardMarkup(
        [
            [club_config["TABLE_FORMAT"].format(i + 1)]
            for i in range(club_config["TABLES"])
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def service_packages():
    return ReplyKeyboardMarkup(
        [
            [f"{package.name} - {package.price} ₴"]
            for package in current_bot.config.SERVICE_PACKAGES
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def date():
    start_date = datetime.date.today()
    delta = club_config["RESERVATION_TIMEDELTA"]

    return ReplyKeyboardMarkup(
        [
            [(start_date + datetime.timedelta(days=i)).strftime("%d-%m")]
            for i in range(delta.days + 1)
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def time():
    return ReplyKeyboardMarkup(
        [["10:10"]], resize_keyboard=True, one_time_keyboard=True
    )


def get_contact():
    button = KeyboardButton(text="Надіслати номер телефону", request_contact=True)

    return ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)


def owner_commands(reservation_id):
    button = InlineKeyboardButton(
        text="Скасувати замовлення", callback_data=f"remove:{reservation_id}"
    )
    return InlineKeyboardMarkup([[button]])
