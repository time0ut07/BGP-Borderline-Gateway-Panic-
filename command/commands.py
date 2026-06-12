from dataclasses import dataclass, field
from typing import Callable

from command.cmd_help import show_help
from command.cmd_exit import exit_app
from conn.conn_run import conn_run
from misc.settings import settings


@dataclass
class Command:
    name: str
    description: str
    handler: Callable | None = None
    subcommands: dict[str, "Command"] = field(default_factory=dict)


# =====================================================
# Handlers
# =====================================================

def call_exit():
    exit_app()

def connection_open():
    conn_run("OPEN")


def connection_update():
    conn_run("UPDATE")


def blackhole():
    print("[+] Running blackhole")


def sniff():
    print("[+] Sniffing network traffic")

def change_setting():
    print("[+] Sniffing network traffic")

def view_setting():
    print("[+] Sniffing network traffic")


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

    ################################# HAVEN DO THIS YET... CHANGE TO 
    # setting change local_ip=127.0.0.1 local_port=1
    #### MAKE SURE HAVE VALIDATION ON 
    ###### 1. IF THE SETTING EXIST IN SETTINGS.TXT
    ###### 2. IF VALUES FOR THE SETTINGS IS VALID
    #### THEN UPDATE
    "setting": Command(
        name="setting",
        description="Modify configuration settings before connection/post-exploit",
        subcommands={
            "change": Command(
                name="change",
                description="Change a settings",
                handler=change_setting,
            ),

            "view": Command(
                name="view",
                description="View all settings",
                handler=view_setting,
            ),
        },
    )
}