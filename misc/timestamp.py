from datetime import datetime


def timestamp() -> str:

    now = datetime.now()
    timestamp = f"[{now.month}/{now.day}/{now.year} {now:%H}:{now:%M}]"

    return timestamp