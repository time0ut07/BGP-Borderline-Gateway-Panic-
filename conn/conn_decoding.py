BGP_ERROR_CODES = {
    1: "Message Header Error",
    2: "OPEN Message Error",
    3: "UPDATE Message Error",
    4: "Hold Timer Expired",
    5: "Finite State Machine Error",
    6: "Cease"
}

BGP_HEADER_SUBCODES = {
    1: "Connection Not Synchronized",
    2: "Bad Message Length",
    3: "Bad Message Type"
}

BGP_OPEN_SUBCODES = {
    1: "Unsupported Version Number",
    2: "Bad Peer AS",
    3: "Bad BGP Identifier",
    4: "Unsupported Optional Parameter",
    5: "Authentication Failure",
    6: "Unacceptable Hold Time"
}

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

def decode_bgp_notification(code:int, subcode:int) -> str:

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