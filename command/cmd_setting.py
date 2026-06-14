from misc.save_setting import save_settings
from misc.grab_settings import get_config
from misc.settings_validation import validate_setting


def cmd_change_setting(args):
    """Usage: setting change key=value key2=value2 ..."""

    if not args:
        print("Usage: setting change key=value key2=value2 ...")
        return

    config = get_config()

    for pair in args:
        if "=" not in pair:
            print(f"[-] Skipping '{pair}', expected format: key=value")
            continue

        key, value = pair.split("=", 1)

        if key not in config:
            print(f"[-] '{key}' is not a valid setting.")
            continue

        valid, fixed_value, error_message = validate_setting(key, value, config)

        if not valid:
            print(f"[-] '{key}': {error_message}")
            continue

        config[key] = fixed_value
        print(f"[+] '{key}' set to '{fixed_value}'")

    save_settings(config)


def cmd_view_setting():
    config = get_config()

    print("\nCurrent settings:")
    for key, value in config.items():
        print(f"  {key} = {value or '(empty)'}")