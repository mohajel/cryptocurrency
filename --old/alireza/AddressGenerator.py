import hashlib as hash
import coincurve
import base58
import os
import random
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
import bitcoin.core as bitC

# VERSION_BYTE = b"\x6f"
VERSION_BYTE_MAINNET = b"0x80"
VERSION_BYTE_TESTNET = b"\x6f"
UNCOMPRESSED_PUBKEY_VERSION = '04'

# random.randint(0,9999999999999).to_bytes(256 , byteorder='big')

# prk = "92rQVTLYXBJVXLJxkh83AZhtNLTWT1bVSeHVQFK2SpZfaU5dyN4"
private_key1 = "65a1c855871842a7e32d4222506e7f70563e11ffbc68231431ced6de159ae15a"
private_key11 = 6199387296283421655423343113918850644817179904262531537313264602583503818558

class PublicAddressGenerator:
    def __init__(self , is_vanity:bool):
        self._private_key = coincurve.PrivateKey()                 # coincurve library uses secp256k1 curve for generating private and public key
        # self._private_key = coincurve.PrivateKey.from_hex(private_key1)               # coincurve library uses secp256k1 curve for generating private and public key
        self._WIF_address = self.WIFconvertor()
        self._public_key = self._private_key.public_key
        self._public_address = self.createPublicAddressFromPublicKey()
        if is_vanity:
            self.vanityAddressGenerator()
    
    def createPublicAddressFromPublicKey(self):
        x = hex(self.public_key.point()[0])
        y = hex(self.public_key.point()[1])
        # concatenated_key = str(x) + str(y)
        concatenated_key = x + y
        hashed_key = VERSION_BYTE_TESTNET + (self.ripemd160Hasher(self.sha256Hasher(concatenated_key).digest()).digest())
        hashed_key = hashed_key + self.createChecksum(hashed_key)
        # print(concatenated_key)
        # print(base58.b58encode(hashed_key).decode('utf-8'))
        return base58.b58encode(hashed_key).decode('utf-8')
        
    # @staticmethod
    def ripemd160Hasher(self , input):
        hasherObj = hash.new("ripemd160")
        if type(input) == str:
            hasherObj.update(input.encode("utf-8"))
        else:
            hasherObj.update(input)
        return hasherObj
        
    # @staticmethod
    def sha256Hasher(self , input):
        hasherObj = hash.new("sha256")
        if type(input) == str:
            hasherObj.update(input.encode("utf-8"))
        else:
            hasherObj.update(input)
        return hasherObj
    
    # @staticmethod
    def createChecksum(self , input):
        checksum = self.sha256Hasher(self.sha256Hasher(input).digest()).digest()[0:4]
        return checksum
    
    def WIFconvertor(self):
        bytes_private_key = self.private_key.to_int().to_bytes(32 , byteorder="big")
        WIF_raw_address = VERSION_BYTE_TESTNET + bytes_private_key
        WIF_raw_address = WIF_raw_address + self.createChecksum(bytes_private_key)
        str1 = base58.b58encode(WIF_raw_address).decode('utf-8')
        return base58.b58encode(WIF_raw_address).decode('utf-8')
        
    
    @property    
    def public_key(self):
            return self._public_key
    
    @property
    def private_key(self):
        return self._private_key
    
    @property
    def public_address(self):
        return self._public_address
    
    @property
    def WIF_address(self):
        return self._WIF_address
    
    def vanityAddressGenerator(self):
        vanityStr = input("Enter your vanity string (3 char): ")
        i = 0
        while (self._public_address[1:4] != vanityStr):
            self._private_key = coincurve.PrivateKey()                  # coincurve library uses secp256k1 curve for generating private and public key
            self._public_key = self._private_key.public_key
            self._public_address = self.createPublicAddressFromPublicKey()
            # print(self._public_address)
            # if(i % 10000 == 0):
            #     print(i)
            i += 1
        
        
    
    
    

# test
if __name__ == "__main__":
    p1 = PublicAddressGenerator(False)

    print(p1.private_key.to_hex())
    print(p1.public_key.point())
    print(p1.public_address)
    print(p1.WIF_address)



