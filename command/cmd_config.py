from misc.save_config import save_config
from misc.grab_config import get_config
from misc.config_validation import validate_config
from misc.add_route import add_route


def cmd_change_config(args: list[str]) -> None:
    """Modify configuration settings from a list of key-value pair

    Parses the command-line arguments and validates each key against
    existing configuration. It then validates the new value format
    and saves the updated configuration file

    Args:
        args (list[str]): A list of strings in 'key=value' format
    """

    if not args:
        print("[*] Usage: config change key=value key2=value2 ...")
        return

    config = get_config()

    for pair in args:
        if "=" not in pair:
            print(f"[-] Skipping '{pair}', expected format: key=value")
            continue

        key, value = pair.split("=", 1)

        if key not in config:
            print(f"[-] '{key}' is not a valid config.")
            continue

        valid, fixed_value, error_message = validate_config(key, value, config)

        if not valid:
            print(f"[-] '{key}': {error_message}")
            continue

        config[key] = fixed_value
        print(f"[+] '{key}' set to '{fixed_value}'")

    save_config(config)


def cmd_view_config() -> None:
    """Retrieve & display current configuration in console

    Fetches the configuration display & prints each key-value pair,
    substituting empty with an '(empty)' placeholder
    """

    config = get_config()

    print("\nCurrent configs:")
    for key, value in config.items():
        print(f"  {key} = {value or '(empty)'}")















def cmd_add_route(args: list[str]) -> None:
    """

    """

    if not args:
        print("[*] Usage: config add-route prefix=x.x.x.x/x next_hop=x.x.x.x")
        print("[*] Optional: as_path=65001,65002 origin=0 med=0")

    params = {}
    for pair in args:
        if "=" not in pair:
            print(f"[-] Skipping '{pair}', expected format: key=value")
            continue
        key, value = pair.split("=", 1)
        params[key.strip()] = value.strip()

    add_route(params)
