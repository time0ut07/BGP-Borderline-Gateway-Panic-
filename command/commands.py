from dataclasses import dataclass, field
from typing import Callable

from command.cmd_help import show_help
from command.cmd_exit import exit_app
from conn.conn_run import conn_run
from command.cmd_config import cmd_change_config, cmd_view_config, cmd_add_route
from command.cmd_clear_log import clear_all_logs
from pe.pe_sniffer import run_sniffer, run_routing
#from pe.sslstrip import start_sslstrip

ACTIVE_CONNECTION = None


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
    global ACTIVE_CONNECTION
    ACTIVE_CONNECTION = conn_run("OPEN")

def connection_update(args=None):
    conn_run("UPDATE", ACTIVE_CONNECTION)


def blackhole(args=None):
    print("[+] Running blackhole")

# For testing oni 
def route(args=None):
    if not args:
        print("[x] Usage: post-exploit route on|off")
        return
    
    if args[0] == "on":
        run_routing(True)

    elif args[0] == "off":
        run_routing(False)

    else:
        print("[x] Invalid option. Use: on or off")


def sniff(args=None):
    if not args:
        print("[x] Usage: post-exploit sniff on|off")
        return
    
    if args[0] == "on":
        run_sniffer(True)

    elif args[0] == "off":
        run_sniffer(False)

    else:
        print("[x] Invalid option. Use: on or off")

def sslstrip(args=None):
    #start_sslstrip()
    pass

def change_config(args):
    cmd_change_config(args)

def view_config(args=None):
    cmd_view_config()

def add_route(args):
    cmd_add_route(args)

def clear_bgp_logs(args=None):
    clear_all_logs('bgp.log')

def clear_traffic_logs(args=None):
    clear_all_logs('traffic.log')


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
            "route": Command(
                name="route",
                description="Route network traffic",
                handler=route,
            ),
            "sslstrip": Command(
                name="sslstrip",
                description="SSLstrip proxy — downgrades HTTPS and captures credentials",
                handler=sslstrip,
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
            "add-route": Command(
            name="add-route",
            description="Manually add a route to route.json",
            handler=add_route,
         ),
        },
    ),

    "clear": Command(
        name="clear",
        description="Clear specified file",
        subcommands={
            "bgp": Command(
                name="bgp",
                description="Clear bgp log file located in ./resources/bgp.log",
                handler=clear_bgp_logs,
            ),
            
            "traffic": Command(
                name="traffic",
                description="Clear traffic log file located in ./resources/traffic.log",
                handler=clear_traffic_logs,
            )
        },
    ),

}