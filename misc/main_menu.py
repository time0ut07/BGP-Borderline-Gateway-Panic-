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
                parts[0] == "config"
                and (parts[1] == "change" or parts[1] == "add-route")
                or
                parts[0] == "post-exploit"
                and (parts[1] == "sniff" or parts[1] == "route")
              ):
                print("[x] This command does not accept arguments")
                continue

            if sub.handler:
                sub.handler(args)
            else:
                print("[x] Subcommand has no action")

        except KeyboardInterrupt:
            print("\n[x] Use 'exit' command to quit")