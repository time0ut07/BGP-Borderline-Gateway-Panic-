from scapy.contrib.bgp import (
    BGP,
    BGPPathAttr,
    BGPPAAS4BytesPath,
    BGPPAASPath,
    BGPCapFourBytesASN,
)


AS_TRANS = 23456
MAX_2OCTET_ASN = 65535


def open_message_asn(asn: int) -> int:
    """
    OPEN messages only have a 2-octet ASN field.
    Use AS_TRANS when the configured ASN needs 4-octet support.
    """

    if asn > MAX_2OCTET_ASN:
        return AS_TRANS

    return asn


def peer_supports_four_byte_asn(open_message_bytes: bytes) -> bool:
    """
    Check whether the peer advertised RFC 6793 4-octet ASN capability.
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
    """
    Build an AS_PATH attribute using the negotiated ASN width.
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
