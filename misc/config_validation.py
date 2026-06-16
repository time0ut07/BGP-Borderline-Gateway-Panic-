import ipaddress


OPTIONAL_FIELDS = [
    "neighbor_ip",
    "neighbor_asn"
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


def validate_config(key, value, config):
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

    if key in ["port", "neighbor_port"]:
        if not is_valid_int_range(value, 1, 65535):
            return False, value, "Port must be between 1 and 65535."
        return True, value, ""

    if  key in ["bgp_id", "neighbor_ip"]:
        if not is_valid_ipv4(value):
            return False, value, f"{key} must be a valid IPv4 address."
        return True, value, ""

    return True, value, ""