import bitcoin.bech32
import bitcoin.wallet
import secrets as sec
from elypticalCurve import *
from generateAddress import produce_WIF_private_key
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

def generate_segwit_address():
    private_key = sec.token_bytes(32)
    generating_point = Point.get_generator_point()
    integer_private_key = int.from_bytes(private_key, "big")
    WIF_private_key = produce_WIF_private_key(private_key, compressed = True)
    public_key = (generating_point * integer_private_key).to_bytes_compressed()
    hashed_public_key = RipeMD160(Sha256(public_key))
    segwit_address = bitcoin.bech32.encode('tb', 0, hashed_public_key)
    return WIF_private_key, segwit_address

