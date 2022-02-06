import datetime

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src import current_bot, helpers


def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["Про клуб 🙌", "Забронювати столик 🗓️"],
            ["Контакти 📲", "Місце розташування 🌍"],
        ],
        resize_keyboard=True,
    )


def tables():
    config = current_bot.config.TABLES

    return ReplyKeyboardMarkup(
        [[config["FORMAT"].format(i + 1)] for i in range(config["AMOUNT"])],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def service_packages():
    return ReplyKeyboardMarkup(
        [
            [f"{package['name']} - {package['price']} ₴"]
            for package in current_bot.config.SERVICE_PACKAGES
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def date(taken_dates=()):
    start_date = datetime.date.today()
    delta = current_bot.config.RESERVATION["TIMEDELTA"]

    keyboard = []
    for i in range(delta.days + 1):
        date = start_date + datetime.timedelta(days=i)
        date = date.strftime("%d-%m")

        if date in taken_dates:
            continue

        keyboard.append([date])

    if not keyboard:
        keyboard = [["Немає вільних місць"]]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def time(taken_times=()):
    config = current_bot.config.RESERVATION
    start = config["OPENING_TIME"]
    end = config["CLOSING_TIME"]
    period = config["TIME_PERIOD"]

    keyboard = []
    for i in range((end - start) // period):
        time = helpers.format_timedelta(start + period * i)

        if time in taken_times:
            continue

        keyboard.append([time])

    if not keyboard:
        keyboard = [["Немає вільних місць"]]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_contact():
    button = KeyboardButton(text="Надіслати номер телефону", request_contact=True)

    return ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)


def owner_commands(reservation_id):
    button = InlineKeyboardButton(
        text="Скасувати бронювання", callback_data=f"remove:{reservation_id}"
    )
    return InlineKeyboardMarkup([[button]])
