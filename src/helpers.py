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


def save_reservation(bot_data, reservation):
    if not bot_data.get("reservations"):
        bot_data["reservations"] = defaultdict(dict)

    bot_data["reservations"][reservation["date"]][
        reservation["time"]
    ] = reservation.copy()

    return True
