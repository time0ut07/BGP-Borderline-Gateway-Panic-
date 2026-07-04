from tabulate import tabulate


def print_config_table(settings: dict, *keys) -> None:
    """Pretty-print configuration values in a tabular format

    Displays configuration key-value pairs using the tabulate library.
    If specific keys are provided, they may be used for filtering in future
    extensions (currently unused).

    Args:
        settings (dict[str, str]): Configuration dictionary to display.
        *keys: Optional filter keys (currently not used).
    """

    table = [[key, value] for key, value in settings.items()]

    print(tabulate(table, headers=["Field", "Value"], tablefmt="grid"))
