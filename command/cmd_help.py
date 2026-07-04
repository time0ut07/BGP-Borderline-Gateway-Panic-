def show_help(commands: dict) -> None:
    """Print a structured help menu displaying all main commands and subcommands

    Iterates through the provided command registry and prints the top-level description
    alongside a strutured tabular view of associated subcommands

    Args:
        commands (dict): A dictionary mapping command names (str) to command objects
    """

    print("\nAvailable Commands\n")

    for cmd_name, cmd in commands.items():
        print(f"{cmd_name}")
        print(f"  {cmd.description}")

        if cmd.subcommands:
            print("  Subcommands:")

            for sub_name, sub in cmd.subcommands.items():
                print(
                    f"    {sub_name:<15} {sub.description}"
                )

        print()
