# In the Name of God

import ecdsa
import hashlib
import base58
import secrets
import sys

def create_random_private_key_hex():
    # Generate a random 256-bit number
    private_key_int = secrets.randbits(256)
    # Convert the number to a hexadecimal string
    private_key_hex = hex(private_key_int)[2:].zfill(64)
    return private_key_hex

def get_address(private_key_hex, testnet = True, mainnet = False):
    # Convert private key from hexadecimal to bytes
    private_key_bytes = bytes.fromhex(private_key_hex)

    # Use secp256k1 elliptic curve to generate public key from private key
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key_bytes = b"\04" + vk.to_string()

    # Hash the public key using SHA-256
    sha256_hash = hashlib.sha256(public_key_bytes).digest()

    # Hash the result again using RIPEMD-160
    ripemd160_hash = hashlib.new("ripemd160", sha256_hash).digest()

    # Add version byte (0x00 for mainnet, 0x6f for testnet) to the RIPEMD-160 hash

    version_ripemd160_hash = b"\x6f" + ripemd160_hash

    # Compute checksum by hashing the version + RIPEMD-160 hash twice and taking the first 4 bytes
    checksum = hashlib.sha256(hashlib.sha256(version_ripemd160_hash).digest()).digest()[:4]

    # Concatenate the version + RIPEMD-160 hash + checksum
    address_bytes = version_ripemd160_hash + checksum

    # Encode the result using Base58Check encoding
    address = base58.b58encode(address_bytes).decode()
    return address


def generate_vanity_address(characters):
    while True:
        address = get_address(create_random_private_key_hex(), testnet=True)
        if address.startswith("m" + characters):
            return address  

if __name__ == "__main__":
    characters = sys.argv[1]
    vanity_address = generate_vanity_address(characters)
    print("Bitcoin Vanity Address:", vanity_address)

