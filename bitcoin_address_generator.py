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

def get_checksum_hex(address_bytes):
    # the first 4 bytes of hash256(prefix + private key + comparision byte)
    checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]


def hex_to_wif(hex, prefix = "ef", compressed = True):
    compressed_hex = ""
    if compressed:
        compressed_hex = "01"
    hex = prefix + hex + compressed_hex 
    bytes_string = bytes.fromhex(hex)
    checksum = hashlib.sha256( hashlib.sha256(bytes_string).digest()).digest()[:4]
    hex = hex + checksum.hex()

    return base58.b58encode(bytes.fromhex(hex)).decode()

def get_address(private_key_hex, type="testnet"):
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


def generate_vanity_address(characters, type = "testnet"):
    while True:
        private_key = create_random_private_key_hex()
        address = get_address(private_key, type="testnet")
        if address[1:].startswith(characters): # may start with m ,2 ,n
            return private_key, address

if __name__ == "__main__":

    if len(sys.argv) == 1: # no input
        private_key = create_random_private_key_hex()
        # private_key = "b808aa179b0a2849abb2a78ab9a7ad1452170e5c97af06d0dcbbbbbcef89a00c"
        address = get_address(private_key, type="testnet")
    else:
        characters = sys.argv[1]
        private_key, address = generate_vanity_address(characters, type="testnet")
        
    print("Private Key Hex:", private_key)
    print("Private Key WIF:", hex_to_wif(private_key, compressed=True))
    print("Bitcoin Address:", address)

