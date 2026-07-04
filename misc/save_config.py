CONFIG_FILE = "resources/config.txt"
"""str: Path to the configuration file stored on disk"""


def save_config(config: dict[str, str]) -> None:
    """Persist configuration dictionary to configuration file

    Writes key-value configuration pairs into 'resources/config.txt' using
    a simple 'key=value' format. Existing file contents are overwritten.

    Args:
        config (dict[str, str]): Configuration dictionary to persist.
    """

    with open(CONFIG_FILE, "w") as file:
        for key, value in config.items():
            file.write(f"{key}={value}\n")
            