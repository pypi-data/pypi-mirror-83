import datetime


def round_down(time: datetime.datetime, round_to: int) -> datetime.datetime:
    t = int(time.timestamp())
    return datetime.datetime.fromtimestamp(t - (t % round_to))

