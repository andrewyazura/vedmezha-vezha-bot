import uuid
from enum import Enum, auto

from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler

from src import current_bot, keyboards, owner


class ReservationStatus(Enum):
    TABLE = auto()
    SERVICE_PACKAGE = auto()
    DATE = auto()
    TIME = auto()
    BOARD_GAME = auto()
    PHONE = auto()


@current_bot.log_update
def make_reservation(update, context):
    context.user_data["current"] = {"id": uuid.uuid4().hex}

    user = update.effective_user
    user.send_message("Оберіть столик", reply_markup=keyboards.tables())

    return ReservationStatus.TABLE


@current_bot.log_update
def get_table(update, context):
    context.user_data["current"]["table"] = update.message.text

    user = update.effective_user
    user.send_message("Оберіть пакет послуг", reply_markup=keyboards.service_packages())

    return ReservationStatus.SERVICE_PACKAGE


@current_bot.log_update
def get_service_package(update, context):
    context.user_data["current"]["service_package"] = update.message.text

    taken = []  # TODO get taken dates

    user = update.effective_user
    user.send_message("Оберіть дату", reply_markup=keyboards.date(taken))

    return ReservationStatus.DATE


@current_bot.log_update
def get_date(update, context):
    context.user_data["current"]["date"] = update.message.text

    taken = []  # TODO get taken times

    user = update.effective_user
    user.send_message("Оберіть час", reply_markup=keyboards.time(taken))

    return ReservationStatus.TIME


@current_bot.log_update
def get_time(update, context):
    context.user_data["current"]["time"] = update.message.text

    user = update.effective_user
    user.send_message(r"Чи є у Вас побажання стосовно настільніх ігор\?")
    user.send_message(r"Пропустити \- /skip", reply_markup=ReplyKeyboardRemove())

    return ReservationStatus.BOARD_GAME


@current_bot.log_update
def skip_board_game(update, context):
    user = update.effective_user
    user.send_message(
        "Для завершення бронювання, нам потрібен ваш номер телефону",
        reply_markup=keyboards.get_contact(),
    )

    return ReservationStatus.PHONE


@current_bot.log_update
def get_board_game(update, context):
    context.user_data["current"]["board_games"] = update.message.text

    return skip_board_game(update, context)


@current_bot.log_update
def get_phone(update, context):
    context.user_data["current"]["phone"] = update.message.contact.phone_number

    reservation = context.user_data["current"]
    current_bot.reservations.insert(reservation)
    owner.send_reservation(reservation)

    user = update.effective_user
    user.send_message("Готово", reply_markup=keyboards.main_menu())
    context.user_data["current"] = {}

    return ConversationHandler.END


@current_bot.log_update
def cancel(update, context):
    user = update.effective_user
    user.send_message(r"Іншим разом\.\.\.", reply_markup=keyboards.main_menu())
    context.user_data["current"] = {}

    return ConversationHandler.END


current_bot.dispatcher.add_handler(
    ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(r"^Забронювати столик 🗓️$"), make_reservation)
        ],
        states={
            ReservationStatus.TABLE: [
                MessageHandler(Filters.regex(r"^Стіл \d+$"), get_table)
            ],
            ReservationStatus.SERVICE_PACKAGE: [
                MessageHandler(Filters.regex(r"^[\w\d ]+ - \d+ ₴"), get_service_package)
            ],
            ReservationStatus.DATE: [
                MessageHandler(Filters.regex(r"\d{2}-\d{2}"), get_date)
            ],
            ReservationStatus.TIME: [
                MessageHandler(Filters.regex(r"\d{2}:\d{2}"), get_time)
            ],
            ReservationStatus.BOARD_GAME: [
                MessageHandler(Filters.text & (~Filters.command), get_board_game),
                CommandHandler("skip", skip_board_game),
            ],
            ReservationStatus.PHONE: [MessageHandler(Filters.contact, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
)
