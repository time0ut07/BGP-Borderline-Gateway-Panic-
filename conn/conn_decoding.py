BGP_ERROR_CODES = {
    1: "Message Header Error",
    2: "OPEN Message Error",
    3: "UPDATE Message Error",
    4: "Hold Timer Expired",
    5: "Finite State Machine Error",
    6: "Cease"
}
"""dict[int, str]: Primary BGP notification error codes as defined by RFC 4271"""


BGP_HEADER_SUBCODES = {
    1: "Connection Not Synchronized",
    2: "Bad Message Length",
    3: "Bad Message Type"
}
"""dict[int, str]: Specific error subcodes for Message Header errors (Code 1)"""


BGP_OPEN_SUBCODES = {
    1: "Unsupported Version Number",
    2: "Bad Peer AS",
    3: "Bad BGP Identifier",
    4: "Unsupported Optional Parameter",
    5: "Authentication Failure",
    6: "Unacceptable Hold Time"
}
"""dict[int, str]: Specific error subcodes for OPEN session establishment messages (Code 2)"""


BGP_UPDATE_SUBCODES = {
    1: "Malformed Attribute List",
    2: "Unrecognized Well-known Attribute",
    3: "Missing Well-known Attribute",
    4: "Attribute Flags Error",
    5: "Attribute Length Error",
    6: "Invalid ORIGIN Attribute",
    7: "AS Routing Loop",
    8: "Invalid NEXT_HOP Attribute",
    9: "Optional Attribute Error",
    10: "Invalid Network Field",
    11: "Malformed AS_PATH"
}
"""dict[int, str]: Specific error subcodes for UPDATE routing path announcement messages (Code 3)"""


BGP_CEASE_SUBCODES = {
    1: "Maximum Number of Prefixes Reached",
    2: "Administrative Shutdown",
    3: "Peer De-configured",
    4: "Administrative Reset",
    5: "Connection Rejected",
    6: "Other Configuration Change",
    7: "Connection Collision Resolution",
    8: "Out of Resources"
}
"""dict[int, str]: Specific error subcodes for Cease notification termination events (Code 6)"""


def decode_bgp_notification(code:int, subcode:int) -> str:
    """Translate raw BGP notification error into a human-readable string

    Parses the primary BGP error category and safety-fetches the explicit sub-error details
    from the corresponding RFC specification maps

    Args:
        code (int): The primary BGP notification error code (1-6)
        subcode (int): The specific error subcode refining the root cause context

    Returns:
        str: A descriptive error string. Returns a generic fallback message 
             if either the primary code or the subcode is undocumented
    """

    if code == 1:
        msg = BGP_HEADER_SUBCODES.get(subcode, "Unknown Header Error")
    elif code == 2:
        msg = BGP_OPEN_SUBCODES.get(subcode, "Unknown Open Error")
    elif code == 3:
        msg = BGP_UPDATE_SUBCODES.get(subcode, "Unknown Update Error")
    elif code == 6:
        msg = BGP_CEASE_SUBCODES.get(subcode, "Unknown Cease Error")
    else:
        msg = "Unknown BGP Error"

    return msg
    