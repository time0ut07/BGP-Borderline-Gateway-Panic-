import ipaddress
import re 

OPTIONAL_FIELDS = [
    "neighbor_ip",
    "neighbor_asn"
]
"""list[str]: Configuration fields that may be left empty during validation"""


def is_valid_ipv4(value:str) -> bool:
    """Validate whether a string represents a valid IPv4 address

    Attempts to parse the supplied value as an IPv4 address.

    Args:
        value (str): The string to validate.

    Returns:
        bool: True if the value is a valid IPv4 address, otherwise False.
    """
    try:
        ipaddress.IPv4Address(value)
        return True
    except ValueError:
        return False


def is_valid_mac(value:str) -> bool:
    """Validate whether a string is formatted as a MAC address

    Checks the supplied value against the standard colon-separated
    hexadecimal MAC address format.

    Args:
        value (str): The string to validate.

    Returns:
        bool: True if the value is a valid MAC address, otherwise False.
    """


    pattern = r'^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$'
    if not re.match(pattern, value):
        return False
    # if value.lower() == "ff:ff:ff:ff:ff:ff":
    #     return False
    return True


def is_valid_int_range(value:str, minimum:int, maximum:int) -> bool:
    """Validate that a string contains an integer within a specified range

    Converts the supplied value to an integer and verifies that it falls
    within the inclusive minimum and maximum bounds.

    Args:
        value (str): The string representation of the integer.
        minimum (int): The minimum permitted value.
        maximum (int): The maximum permitted value.

    Returns:
        bool: True if the value is a valid integer within the specified
            range, otherwise False.
    """

    try:
        number = int(value)
        return minimum <= number <= maximum
    except ValueError:
        return False


def validate_config(key:str, value:str, config:dict) -> tuple[bool, str, str]:
    """Validate a configuration field against predefined constraints

    Performs field-specific validation for supported configuration options,
    including BGP version, Autonomous System Numbers, hold timers, ports,
    IPv4 addresses, and MAC addresses. Optional fields may be left empty.

    Args:
        key (str): Configuration field name.
        value (str): User-supplied value to validate.
        config (dict): Complete configuration dictionary. Reserved for
            validations requiring additional configuration context.

    Returns:
        tuple[bool, str, str]: A tuple containing the validation result,
            the normalized value, and an error message if validation fails.
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

    if  key in ["bgp_id", "neighbor_ip","route_dest_ip"]:
        if not is_valid_ipv4(value):
            return False, value, f"{key} must be a valid IPv4 address."
        return True, value, ""
        
    if key == "route_dest_mac":
        if not is_valid_mac(value):
            return False, value, "route_dest_mac must be a valid MAC address (xx:xx:xx:xx:xx:ff) and cannot be broadcast."
        return True, value.lower(), ""

    return True, value, ""