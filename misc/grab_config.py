def get_config(config_list:list = None) -> dict:
    """
    Get configuration value from resources/config.txt
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