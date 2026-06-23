from datetime import datetime


def timestamp() -> str:

    now = datetime.now()
    ms = now.microsecond // 1000
    timestamp = f"[{now.month}/{now.day}/{now.year} {now:%H}:{now:%M}:{now:%S}]"

    return timestamp