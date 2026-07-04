from misc.grab_config import get_config
from misc.timestamp import timestamp

def handle_log(msg:str, file:str) -> None:
    """Append a timestamped log entry to a resource log file

    Writes a formatted log message containing the current timestamp and the
    provided message into a file inside the './resources/' directory.

    Args:
        msg (str): Log message content to record.
        file (str): Target log file name (e.g. "bgp.log").
    """

    with open(f"./resources/{file}", "a") as f:
        f.write(f"{timestamp()} {msg}\n")
