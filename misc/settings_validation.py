import ipaddress


OPTIONAL_FIELDS = [
    "local_ip",
    "neighbor_ip",
    "neighbor_asn",
    "announce_prefix",
    "prefix_length",
    "next_hop",
    "as_path",
    "withdraw_prefix",
    "withdraw_prefix_length",
    "local_pref",
    "med",
    "community"
]


def is_valid_ipv4(value):
    try:
        ipaddress.IPv4Address(value)
        return True
    except ValueError:
        return False


def is_valid_int_range(value, minimum, maximum):
    try:
        number = int(value)
        return minimum <= number <= maximum
    except ValueError:
        return False


def validate_setting(key, value, config):
    """
    Returns:
    (is_valid, fixed_value, error_message)
    """

    value = value.strip()

    if value == "" and key in OPTIONAL_FIELDS:
        return True, value, ""

    if key == "version":
        if value != "4":
            return False, value, "Version must be 4."
        return True, value, ""

    if key in ["asn", "neighbor_asn"]:
        if not is_valid_int_range(value, 1, 4294967295):
            return False, value, "ASN must be between 1 and 4294967295."
        return True, value, ""

    if key == "hold_time":
        if not value.isdigit():
            return False, value, "Hold time must be a number."

        hold_time = int(value)

        if hold_time != 0 and hold_time < 3:
            return False, value, "Hold time must be 0 or at least 3 seconds."

        return True, value, ""

    if key == "keepalive_interval":
        if not value.isdigit():
            return False, value, "Keepalive interval must be a number."

        keepalive = int(value)

        if keepalive <= 0:
            return False, value, "Keepalive interval must be greater than 0."

        hold_time = config.get("hold_time", "")

        if hold_time.isdigit():
            hold_time = int(hold_time)

            if hold_time != 0 and keepalive >= hold_time:
                return False, value, "Keepalive interval must be less than hold time."

        return True, value, ""

    if key in ["local_port", "neighbor_port"]:
        if not is_valid_int_range(value, 1, 65535):
            return False, value, "Port must be between 1 and 65535."
        return True, value, ""

    if key in ["bgp_id", "local_ip", "neighbor_ip", "next_hop"]:
        if not is_valid_ipv4(value):
            return False, value, f"{key} must be a valid IPv4 address."
        return True, value, ""

    if key == "origin":
        allowed = ["IGP", "EGP", "INCOMPLETE"]
        value = value.upper()

        if value not in allowed:
            return False, value, "Origin must be IGP, EGP, or INCOMPLETE."

        return True, value, ""

    if key in ["prefix_length", "withdraw_prefix_length"]:
        if not is_valid_int_range(value, 0, 32):
            return False, value, "Prefix length must be between 0 and 32."
        return True, value, ""

    if key in ["announce_prefix", "withdraw_prefix"]:
        if not is_valid_ipv4(value):
            return False, value, f"{key} must be a valid IPv4 network address."
        return True, value, ""

    if key in ["local_pref", "med"]:
        if not is_valid_int_range(value, 0, 4294967295):
            return False, value, f"{key} must be between 0 and 4294967295."
        return True, value, ""

    if key in ["as_path", "community"]:
        return True, value, ""

    return True, value, ""