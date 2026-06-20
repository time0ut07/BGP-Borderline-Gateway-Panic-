from misc.grab_config import get_config
from misc.timestamp import timestamp

def handle_log(msg:str, file:str) -> int:

    with open(f"./resources/{file}", "a") as f:
        f.write(f"{timestamp()} {msg}\n")

    return 0