from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["Про клуб 🙌", "Забронювати столик 🗓️"],
            ["Контакти 📲", "Місце розташування 🌍"],
        ]
    )
