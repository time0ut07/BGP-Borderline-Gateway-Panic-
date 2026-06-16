from dataclasses import dataclass, field
from typing import Callable

from command.cmd_help import show_help
from command.cmd_exit import exit_app
from conn.conn_run import conn_run
from command.cmd_config import cmd_change_config, cmd_view_config
from command.cmd_clear_log import clear_all_logs
from conn.parse_BGP import get_connectivity

# ACTIVE_CONNECTION = None


@dataclass
class Command:
    name: str
    description: str
    handler: Callable | None = None
    subcommands: dict[str, "Command"] = field(default_factory=dict)


# =====================================================
# Handlers
# =====================================================

def call_exit(args=None):
    exit_app()

def connection_open(args=None):
    #global ACTIVE_CONNECTION
    conn_run("OPEN")

def connection_update(args=None):
    conn_run("UPDATE", get_connectivity)


def blackhole(args=None):
    print("[+] Running blackhole")


def sniff(args=None):
    print("[+] Sniffing network traffic")

def change_config(args):
    cmd_change_config(args)

def view_config(args=None):
    cmd_view_config()

def clear_logs(args=None):
    clear_all_logs()


# =====================================================
# Commands
# =====================================================

COMMANDS = {

    "exit": Command(
        name="exit",
        description="Exit gracefully",
        handler=call_exit,
    ),

    "connection": Command(
        name="connection",
        description="BGP Connection operations",
        subcommands={
            "open": Command(
                name="open",
                description="Open connection",
                handler=connection_open,
            ),
            "update": Command(
                name="update",
                description="Update connection",
                handler=connection_update,
            ),
        },
    ),

    "post-exploit": Command(
        name="post-exploit",
        description="Post exploitation actions",
        subcommands={
            "blackhole": Command(
                name="blackhole",
                description="Start blackhole attack",
                handler=blackhole,
            ),
            "sniff": Command(
                name="sniff",
                description="Sniff network traffic",
                handler=sniff,
            ),
        },
    ),

    "config": Command(
        name="config",
        description="Modify configuration configs before connection/post-exploit",
        subcommands={
            "change": Command(
                name="change",
                description="Change a configuration",
                handler=change_config,
            ),

            "view": Command(
                name="view",
                description="View all configs",
                handler=view_config,
            ),
        },
    ),

    "clear": Command(
        name="clear",
        description="Clear specified file",
        subcommands={
            "logs": Command(
                name="logs",
                description="Clear log file located in ./resources/logs.txt",
                handler=clear_logs,
            ),
        },
    ),

}