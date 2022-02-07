import logging
from datetime import date

from tinydb import Query

from src import current_bot


def _check_date(val, today):
    d, m = val.split("-")
    return date(year=today.year, month=int(m), day=int(d)) < today


def clear_reservations(context):
    logger = logging.getLogger("telegram_bot")
    logger.debug("Removing old reservations")
    ids = current_bot.reservations.remove(Query().date.test(_check_date, date.today()))
    logger.debug(f"Removed {len(ids)} old reservations")


current_bot.job_queue.run_repeating(
    clear_reservations,
    interval=current_bot.config.RESERVATION["CLEAR_INTERVAL"],
    first=1,
)
