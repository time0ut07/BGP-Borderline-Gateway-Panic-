import sys

from command.commands import COMMANDS
from command.cmd_help import show_help


def main_menu():
    """Run the interactive BGP command-line interface

    Implements a REPL-style command interpreter driven by the COMMANDS
    registry. Supports hierarchical commands with optional subcommands and
    argument validation for selected command groups.

    Features:
        - Top-level command parsing (e.g. config, connection, exit)
        - Subcommand dispatch via COMMANDS structure
        - Built-in help system
        - Argument validation for restricted command types
        - Graceful handling of invalid input and keyboard interrupts
    """

    while True:
        try:
            raw = input("\nVORTEX >> ").strip()

            if not raw:
                continue

            if raw.lower() == "help":
                show_help(COMMANDS)
                continue

            parts = raw.split()

            cmd = COMMANDS.get(parts[0])

            if not cmd:
                print(f"[x] Unknown command: {parts[0]}")
                continue

            # Commands without subcommands (e.g. exit)
            if not cmd.subcommands:
                if cmd.handler:
                    cmd.handler()
                else:
                    print("[x] Command has no action")
                continue

            # User typed: connection / config
            if len(parts) < 2:
                print(f"\n{cmd.name} commands:")

                for subcmd in cmd.subcommands.values():
                    print(f"  {subcmd.name:<12} {subcmd.description}")

                continue

            sub = cmd.subcommands.get(parts[1])

            if not sub:
                print(f"[x] Unknown subcommand: {parts[1]}")

                print(f"\nAvailable {cmd.name} commands:")

                for subcmd in cmd.subcommands.values():
                    print(f"  {subcmd.name:<12} {subcmd.description}")

                continue

            args = parts[2:]

            # Only allow args for: config change
            if args and not (
                (parts[0] == "config" and parts[1] in ["change", "add-route", "remove-route"])
                or
                (parts[0] == "post-exploit" and parts[1] in ["sniff", "route"])
              ):
                print("[x] This command does not accept arguments")
                continue

            if sub.handler:
                sub.handler(args)
            else:
                print("[x] Subcommand has no action")

        except KeyboardInterrupt:
            print("\n[x] Use 'exit' command to quit")
            