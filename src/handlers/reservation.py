import uuid
from enum import Enum, auto

from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler

from src import current_bot, helpers, keyboards, owner


class ReservationStatus(Enum):
    NAME = auto()
    TABLE = auto()
    SERVICE_PACKAGE = auto()
    DATE = auto()
    TIME = auto()
    AMOUNT = auto()
    BOARD_GAME = auto()
    PHONE = auto()


@current_bot.log_update
def make_reservation(update, context):
    context.user_data["current"] = {"id": uuid.uuid4().hex}

    user = update.effective_user
    user.send_message("Введіть ім'я", reply_markup=ReplyKeyboardRemove())
    user.send_message("Скасувати - /cancel")

    return ReservationStatus.NAME


@current_bot.log_update
def get_name(update, context):
    context.user_data["current"]["name"] = update.message.text

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

    taken = helpers.get_taken_dates(context.user_data["current"])

    user = update.effective_user
    user.send_message("Оберіть дату", reply_markup=keyboards.date(taken))

    return ReservationStatus.DATE


@current_bot.log_update
def get_date(update, context):
    context.user_data["current"]["date"] = update.message.text

    taken = helpers.get_taken_times(context.user_data["current"])

    user = update.effective_user
    user.send_message("Оберіть час", reply_markup=keyboards.time(taken))

    return ReservationStatus.TIME


@current_bot.log_update
def get_time(update, context):
    context.user_data["current"]["time"] = update.message.text

    user = update.effective_user
    user.send_message("Введіть кількість людей")

    return ReservationStatus.AMOUNT


@current_bot.log_update
def get_amount(update, context):
    context.user_data["current"]["amount"] = update.message.text

    user = update.effective_user
    user.send_message("Чи є у Вас побажання стосовно настільніх ігор?")
    user.send_message("Пропустити - /skip", reply_markup=ReplyKeyboardRemove())

    return ReservationStatus.BOARD_GAME


@current_bot.log_update
def skip_board_game(update, context):
    user = update.effective_user
    user.send_message("Для завершення бронювання, нам потрібен ваш номер телефону")

    return ReservationStatus.PHONE


@current_bot.log_update
def get_board_game(update, context):
    context.user_data["current"]["board_games"] = update.message.text

    return skip_board_game(update, context)


@current_bot.log_update
def get_phone(update, context):
    context.user_data["current"]["phone"] = update.message.text

    reservation = context.user_data["current"]
    current_bot.reservations.insert(reservation)
    owner.send_reservation(reservation)

    user = update.effective_user
    user.send_message("Готово", reply_markup=keyboards.main_menu())
    user.send_message(
        f"{reservation['table']}\n"
        f"<b>Дата:</b> {reservation['date']}\n"
        f"<b>Час:</b> {reservation['time']}\n"
        f"<b>Ігри:</b> {reservation.get('board_games') or 'не вказано'}\n"
    )
    context.user_data["current"] = {}

    return ConversationHandler.END


@current_bot.log_update
def cancel(update, context):
    user = update.effective_user
    user.send_message("Іншим разом...", reply_markup=keyboards.main_menu())
    context.user_data["current"] = {}

    return ConversationHandler.END


current_bot.dispatcher.add_handler(
    ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(r"^Забронювати столик 🗓️$"), make_reservation)
        ],
        states={
            ReservationStatus.NAME: [
                MessageHandler(Filters.regex(r"^[\w ]+$"), get_name)
            ],
            ReservationStatus.TABLE: [
                MessageHandler(Filters.regex(r"^Стіл \d+$"), get_table)
            ],
            ReservationStatus.SERVICE_PACKAGE: [
                MessageHandler(
                    Filters.regex(r"^[\w\d ]+ - \d+ ₴$"), get_service_package
                )
            ],
            ReservationStatus.DATE: [
                MessageHandler(Filters.regex(r"^\d{2}-\d{2}$"), get_date)
            ],
            ReservationStatus.TIME: [
                MessageHandler(Filters.regex(r"^\d{2}:\d{2}$"), get_time)
            ],
            ReservationStatus.AMOUNT: [
                MessageHandler(Filters.regex(r"^\d+$"), get_amount)
            ],
            ReservationStatus.BOARD_GAME: [
                MessageHandler(Filters.text & (~Filters.command), get_board_game),
                CommandHandler("skip", skip_board_game),
            ],
            ReservationStatus.PHONE: [
                MessageHandler(
                    Filters.regex(current_bot.config.PHONE_NUMBER_REGEX), get_phone
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(Filters.regex("^Немає вільних місць$"), cancel),
        ],
        allow_reentry=True,
    )
)
