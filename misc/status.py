def get_status(status:str) -> bool:
    """Retrieve a boolean status flag from the local status file

    Reads key-value pairs from './resources/status' and returns the
    boolean state of the requested status key.

    The file uses 'key=0' or 'key=1' format, where '1' represents
    True and any other value is treated as False.

    Args:
        status (str): The status key to query.

    Returns:
        bool: True if the status exists and is set to "1", otherwise False.
    """

    with open("./resources/status", "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if key == status:
                if value == "1":
                    return True

    return False


def change_status(status:str, value:int) -> None:
    """Update or insert a status flag in the local status file

    Modifies './resources/status' by updating an existing key or appending
    a new one if it does not exist. Status values are stored as "1" or "0".

    Args:
        status (str): The status key to modify.
        value (int): Integer value representing the status (0 or 1).
    """

    new_value = "1" if value else "0"
    updated = False
    lines = []

    try:
        with open("./resources/status", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    for i in range(len(lines)):
        line = lines[i].strip()

        if not line or line.startswith("#"):
            continue

        if "=" in line:
            key, _ = line.split("=", 1)
            key = key.strip()

            if key == status:
                lines[i] = f"{status}={new_value}\n"
                updated = True

    if not updated:
        lines.append(f"{status}={new_value}\n")

    # write back
    with open("./resources/status", "w") as f:
        f.writelines(lines)
