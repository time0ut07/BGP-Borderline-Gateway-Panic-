def get_config(config_list:list[str] | None = None) -> dict[str, str]:
    """Load configuration values from the local config file

    Reads key-value pairs from ``./resources/config.txt`` and optionally
    filters them based on a provided whitelist of configuration keys.

    Lines beginning with `#` or empty lines are ignored.

    Args:
        config_list (list[str] | None): Optional list of configuration keys
            to retrieve. If None, all configuration values are loaded.

    Returns:
        dict[str, str]: Dictionary containing requested configuration keys
            mapped to their corresponding string values.
    """
    
    config_dict = {}

    with open("./resources/config.txt", 'r') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue
            
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if config_list is None or key in config_list:
                config_dict[key] = value

        return config_dict
