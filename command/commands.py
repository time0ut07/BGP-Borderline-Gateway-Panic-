from dataclasses import dataclass, field

from command.cmd_help import show_help
from command.cmd_exit import exit_app
from conn.conn_run import conn_run
from command.cmd_config import cmd_change_config, cmd_view_config, cmd_add_route
from command.cmd_clear_log import clear_all_logs
from pe.pe_sniffer import run_sniffer, run_routing

ACTIVE_CONNECTION = None


@dataclass
class Command:
    """Data blueprint representing a CLI command & subcommand.

    Attributes:
        name (str): The unique keyword token used to trigger the command.
        description (str): A brief summary of what the command executes.
        handler (Callable | None): The callback function executed when called.
        subcommands (dict[str, Command]): A mapping of nested subcommand keywords 
    """

    name: str
    description: str
    handler: Callable | None = None
    subcommands: dict[str, "Command"] = field(default_factory=dict)


# =====================================================
# Handlers
# =====================================================

def call_exit(args:list[str] | None = None) -> None:
    """Wrapper function to invoke the main application graceful shutdown routine
    """
    
    exit_app()


def connection_open(args:list[str] | None = None) -> None:
    """Initialize and open an active BGP network connection session
    """
    
    global ACTIVE_CONNECTION
    ACTIVE_CONNECTION = conn_run("OPEN")


def connection_update(args:list[str] | None = None) -> None:
    """Send an update packet over the currently active BGP connection session
    """

    conn_run("UPDATE", ACTIVE_CONNECTION)


def route(args:list[str] | None = None) -> None:
    """Toggle background routing engine on or off.

    Args:
        args (list[str] | None): CLI positional arguments, expects ['on'] or ['off']
    """

    if not args:
        print("[x] Usage: post-exploit route on|off")
        return
    
    if args[0] == "on":
        run_routing(True)

    elif args[0] == "off":
        run_routing(False)

    else:
        print("[x] Invalid option. Use: on or off")


def sniff(args:list[str] | None = None) -> None:
    """Toggle background raw packet sniffing

    Args:
        args (list[str] | None): CLI positional arguments. Expects ['on'] or ['off'].
    """

    if not args:
        print("[x] Usage: post-exploit sniff on|off")
        return
    
    if args[0] == "on":
        run_sniffer(True)

    elif args[0] == "off":
        run_sniffer(False)

    else:
        print("[x] Invalid option. Use: on or off")
        

def change_config(args:list[str] | None = None) -> None:
    """Forward modification string pairs to configuration file

    Args:
        args (list[str]): List of configuration target strings (e.g., ['key=value'])
    """

    cmd_change_config(args)


def view_config(args:list[str] | None = None) -> None:
    """Fetch and print the current live configuration list
    """

    cmd_view_config()


def add_route(args:list[str] | None = None) -> None:
    """Forward explicit parameter arrays to the routing table function

    Args:
        args (list[str]): Explicit prefix configuration strings
    """
    cmd_add_route(args)


def clear_bgp_logs(args:list[str] | None = None) -> None:
    """Truncate all text contents in './resources/bgp.log'
    """
    clear_all_logs('bgp.log')


def clear_traffic_logs(args:list[str] | None = None) -> None:
    """Truncate all text contents in './resources/traffic.log'
    """

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
