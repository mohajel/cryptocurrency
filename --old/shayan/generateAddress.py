import secrets as sec
import base58
import bitcoin.wallet
from utils import Sha256, RipeMD160, calculate_checksum
from elypticalCurve import *

def produce_WIF_private_key(private_key, compressed = False):
    extended = b"\xef" + private_key
    if(compressed):
        extended = extended + b"\x01"
    checksum = calculate_checksum(extended)
    WIF_private_key_not_encoded = extended + checksum
    return base58.b58encode(WIF_private_key_not_encoded)


def produce_address(private_key):
    generating_point = Point.get_generator_point()
    integer_private_key = int.from_bytes(private_key, "big")
    public_key = (generating_point * integer_private_key).to_bytes()
    hashed_value = RipeMD160(Sha256(public_key))
    extended_address = b"\x6f" + hashed_value
    checksumed_address = extended_address + calculate_checksum(extended_address)
    return public_key, base58.b58encode(checksumed_address)

def produce_keys():
    private_key = sec.token_bytes(32)
    WIF_private_key = produce_WIF_private_key(private_key)
    public_key, address = produce_address(private_key)
    return WIF_private_key, address

