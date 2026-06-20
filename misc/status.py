def get_status(status: str) -> bool:
    """
    Get a status value from resources/status
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


def change_status(status:str, value:int) -> bool:
    """
    Update a status value in resources/status
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

    return True