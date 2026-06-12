from tabulate import tabulate
from misc.settings_validation import validate_setting

SETTINGS_FILE = "resources/settings.txt"

SETTING_GROUPS = {
    "OPEN Message Settings": [
        "version",
        "asn",
        "hold_time",
        "bgp_id"
    ],
    "Peer Connection Settings": [
        "local_ip",
        "neighbor_ip",
        "neighbor_asn",
        "local_port",
        "neighbor_port",
        "keepalive_interval"
    ],
    "UPDATE Message Settings": [
        "announce_prefix",
        "prefix_length",
        "next_hop",
        "origin"
    ],
    "Route Withdrawal Settings": [
        "withdraw_prefix",
        "withdraw_prefix_length"
    ],
    "Path Attributes Settings": [
        "as_path",
        "local_pref",
        "med",
        "community"
    ]
}


def load_settings():
    config = {}

    try:
        with open(SETTINGS_FILE, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()

    except FileNotFoundError:
        print(f"Error: {SETTINGS_FILE} not found.")

    return config


def save_settings(config):
    with open(SETTINGS_FILE, "w") as file:
        for key, value in config.items():
            file.write(f"{key}={value}\n")


def display_group_settings(config, group_name):
    fields = SETTING_GROUPS[group_name]
    table = []

    for index, key in enumerate(fields, start=1):
        table.append([index, key, config.get(key, "")])

    print(f"\n===== {group_name.upper()} =====\n")
    print(tabulate(table, headers=["No.", "Setting", "Value"], tablefmt="grid"))


def settings():
    while True:
        config = load_settings()
        group_names = list(SETTING_GROUPS.keys())

        print("\n===== SETTINGS MENU =====\n")

        for index, group in enumerate(group_names, start=1):
            print(f"{index}. {group}")

        try:
            group_choice = int(input("\nSelect category('6' to exit): "))

            if group_choice == 6:
                break

            if group_choice < 1 or group_choice > len(group_names):
                print("Invalid category.")
                continue

            selected_group = group_names[group_choice - 1]

            while True:
                display_group_settings(config, selected_group)

                print("\n0. Back")

                setting_choice = int(input("\nSelect setting to modify('0' to exit): "))

                if setting_choice == 0:
                    break

                fields = SETTING_GROUPS[selected_group]

                if setting_choice < 1 or setting_choice > len(fields):
                    print("Invalid setting.")
                    continue

                selected_key = fields[setting_choice - 1]
                current_value = config.get(selected_key, "")

                new_value = input(
                    f"Enter new value for '{selected_key}' "
                    f"(current: {current_value}): "
                )

                valid, fixed_value, error_message = validate_setting(
                    selected_key,
                    new_value,
                    config
                )

                if not valid:
                    print(f"\nInvalid value: {error_message}")
                    continue

                config[selected_key] = fixed_value
                save_settings(config)

                print(f"\n'{selected_key}' updated successfully.")

        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    settings()