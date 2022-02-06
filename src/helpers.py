from tinydb import Query

from src import current_bot

q = Query()


def get_taken_dates(reservation):
    reservations = current_bot.reservations.search(q.table == reservation["table"])

    # for r in reservations:
    #     if r.
    return []


def get_taken_times(reservation):
    reservations = current_bot.reservations.search(
        (q.table == reservation["table"]) & (q.date == reservation["date"])
    )

    return [r["time"] for r in reservations]
