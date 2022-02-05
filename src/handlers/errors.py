import traceback

from telegram import ParseMode

from src import current_bot


def error_handler(update, context):
    exc_info = context.error

    current_bot.logger.error(msg="Exception:", exc_info=exc_info)

    error_traceback = traceback.format_exception(
        type(exc_info), exc_info, exc_info.__traceback__
    )

    message = (
        f"<i>user_data</i><pre>{context.user_data}</pre>\n"
        f"<i>chat_data</i><pre>{context.chat_data}</pre>\n"
        f"<i>bot_data</i><pre>{context.bot_data}</pre>\n\n"
        "<i>exception</i>\n"
        f"<pre>{''.join(error_traceback)}</pre>"
    )

    context.bot.send_message(chat_id=526698748, text=message, parse_mode=ParseMode.HTML)


current_bot.dispatcher.add_error_handler(error_handler)
