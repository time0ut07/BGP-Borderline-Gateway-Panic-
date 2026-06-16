CONFIG_FILE = "resources/config.txt"


def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        for key, value in config.items():
            file.write(f"{key}={value}\n")