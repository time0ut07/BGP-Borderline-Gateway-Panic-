import sys

from command.commands import COMMANDS
from command.cmd_help import show_help


def main_menu():
    """
    Command-based interface (fully driven by COMMANDS)
    """

    while True:
        try:
            raw = input("\nBGP >> ").strip()

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

            if not cmd.subcommands:
                if cmd.handler:
                    cmd.handler()
                else:
                    print("[x] Command has no action")
                continue

                print("[x] Missing subcommand")
                continue

            sub = cmd.subcommands.get(parts[1])

            if not sub:
                print(f"[x] Unknown subcommand: {parts[1]}")
                continue

            if sub.handler:
                sub.handler()
            else:
                print("[x] Subcommand has no action")

        except KeyboardInterrupt:
            print("\n[x] Use 'exit' command to quit")