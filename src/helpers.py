from datetime import timedelta

from tinydb import Query

from src import current_bot

q = Query()


def get_service_package(package_string):
    for i in current_bot.config.SERVICE_PACKAGES:
        if f"{i['name']} - {i['price']} ₴" == package_string:
            return i

    return None


def get_taken_dates(reservation):
    reservations = current_bot.reservations.search(q.table == reservation["table"])

    taken = []

    for r in reservations:
        p = get_service_package(r["service_package"])
        if p["timedelta"].days == 1:
            taken.append(r["date"])

    return taken


def get_taken_times(reservation):
    period = current_bot.config.CLUB["TIME_PERIOD"]
    reservations = current_bot.reservations.search(
        (q.table == reservation["table"]) & (q.date == reservation["date"])
    )

    taken = []

    for r in reservations:
        h, m = r["time"].split(":")
        start = timedelta(hours=int(h), minutes=int(m))
        duration = get_service_package(r["service_package"])["timedelta"]

        for i in range(duration // period):
            time = format_timedelta(start + period * i)
            taken.append(time)

    return taken


def format_timedelta(timedelta):
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}"
