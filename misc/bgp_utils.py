from scapy.contrib.bgp import (
    BGP,
    BGPPathAttr,
    BGPPAAS4BytesPath,
    BGPPAASPath,
    BGPCapFourBytesASN,
)


AS_TRANS = 23456
"""int: Reserved transition Autonomous System Number defined by RFC 6793"""

MAX_2OCTET_ASN = 65535
"""int: Maximum Autonomous System Number representable in the legacy 2-octet ASN field"""


def open_message_asn(asn: int) -> int:
    """Convert an ASN for use in a BGP OPEN message

    Determines whether the configured Autonomous System Number can be
    represented in the legacy 2-octet ASN field. If the ASN exceeds the
    supported range, the reserved AS_TRANS value is returned as required by
    RFC 6793.

    Args:
        asn (int): The local Autonomous System Number.

    Returns:
        int: The original ASN if it fits within 2 octets, otherwise the
            AS_TRANS placeholder value.
    """

    if asn > MAX_2OCTET_ASN:
        return AS_TRANS

    return asn


def peer_supports_four_byte_asn(open_message_bytes: bytes) -> bool:
    """Determine whether a peer advertises 4-octet ASN capability

    Parses a received BGP OPEN message and inspects its advertised capability
    list for the RFC 6793 Four-Byte ASN capability.

    Args:
        open_message_bytes (bytes): Raw bytes containing a serialized BGP
            OPEN message.

    Returns:
        bool: True if the peer supports 4-octet ASNs, otherwise False.
    """

    try:
        pkt = BGP(open_message_bytes)
    except Exception:
        return False

    if getattr(pkt, "type", None) != 1:
        return False

    for opt_param in getattr(pkt.payload, "opt_params", []):
        capability = getattr(opt_param, "param_value", None)
        if isinstance(capability, BGPCapFourBytesASN):
            return True

    return False


def build_as_path_attr(asn: int,target_asn:int, use_four_byte_encoding: bool) -> BGPPathAttr:
    """Construct a BGP AS_PATH attribute using the negotiated ASN format

    Builds an AS_PATH path attribute encoded with either the legacy 2-octet
    format or the RFC 6793 4-octet format depending on the capabilities
    negotiated with the remote peer.

    Args:
        asn (int): The local Autonomous System Number.
        target_asn (int): The destination or neighboring Autonomous System
            Number to include in the AS path.
        use_four_byte_encoding (bool): Indicates whether 4-octet ASN encoding
            was successfully negotiated during the BGP OPEN exchange.

    Returns:
        BGPPathAttr: A Scapy BGP AS_PATH path attribute ready for inclusion in
            a BGP UPDATE message.
    """

    if use_four_byte_encoding:
        attribute = BGPPAAS4BytesPath(segments=[
            BGPPAAS4BytesPath.ASPathSegment(
                segment_type=2,
                segment_value=[asn,65001],
            )
        ])
    else:
        if asn > MAX_2OCTET_ASN:
            raise ValueError(
                "Peer did not advertise 4-octet ASN support, but local ASN exceeds 65535."
            )

        attribute = BGPPAASPath(segments=[
            BGPPAASPath.ASPathSegment(
                segment_type=2,
                segment_value=[asn,target_asn],
            )
        ])

    return BGPPathAttr(
        type_flags=0x40,
        type_code=2,
        attribute=attribute,
    )
