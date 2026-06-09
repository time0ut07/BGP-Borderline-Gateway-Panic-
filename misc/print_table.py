from tabulate import tabulate


def print_settings_table(settings: dict, *keys) -> None:
    """
    Print out key value with tabulate
    """

    table = [[key, value] for key, value in settings.items()]

    print(tabulate(table, headers=["Field", "Value"], tablefmt="grid"))

    return None