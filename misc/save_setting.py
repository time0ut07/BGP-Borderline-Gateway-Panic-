SETTINGS_FILE = "resources/settings.txt"


def save_settings(config):
    with open(SETTINGS_FILE, "w") as file:
        for key, value in config.items():
            file.write(f"{key}={value}\n")