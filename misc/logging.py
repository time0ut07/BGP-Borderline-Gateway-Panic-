from misc.grab_settings import get_config
from misc.timestamp import timestamp

def handle_log(msg:str) -> int:

    with open("./resources/logs.txt", "a") as f:
        f.write(f"{timestamp()} {msg}\n")

    return 0