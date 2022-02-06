from collections import defaultdict


def find_reservation(bot_data, _id):
    reservations = bot_data["reservations"]

    for date, value in reservations.items():
        for time, reservation in value.items():
            if reservation["id"] == _id:
                return date, time

    return False


def delete_reservation(bot_data, _id):
    reservation = find_reservation(bot_data, _id)

    if not reservation:
        return False

    date, time = reservation
    del bot_data["reservations"][date][time]
    return True


def check_bot_data(bot_data):
    if not bot_data.get("reservations"):
        bot_data["reservations"] = defaultdict(dict)


def save_reservation(bot_data, reservation):
    check_bot_data(bot_data)

    bot_data["reservations"][reservation["date"]][
        reservation["time"]
    ] = reservation.copy()

    return True


def get_taken_times(bot_data, date):
    check_bot_data(bot_data)

    return [time for time, value in bot_data["reservations"][date].items() if value]
