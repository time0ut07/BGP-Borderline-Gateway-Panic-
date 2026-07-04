from datetime import datetime


def timestamp() -> str:
    """Generate a formatted timestamp string for logging

    Produces a human-readable timestamp in the format:
    '[MM/DD/YYYY HH:MM:SS]'

    Returns:
        str: The formatted timestamp string.
    """

    now = datetime.now()
    ms = now.microsecond // 1000
    timestamp = f"[{now.month}/{now.day}/{now.year} {now:%H}:{now:%M}:{now:%S}]"

    return timestamp
