def show_help(commands):
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