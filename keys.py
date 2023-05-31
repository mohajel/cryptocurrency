from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
from bitcoin.core import b2x, Hash
from utils import *

bitcoin.SelectParams("testnet")

key1 = CBitcoinSecret("cTkSSMQbC9pxYKf1iRPTZ69pjcWP1bS2vAGhDMPV32izxKXtiU6u")
key1_addr = P2PKHBitcoinAddress.from_pubkey(key1.pub)

key2 = CBitcoinSecret("cNuJHQPJ417DT55KgNbvVNzKXXLX4UFxoRb1gb9sRx1Ga9oxaVuK")
key2_addr = P2PKHBitcoinAddress.from_pubkey(key2.pub)

key3 = CBitcoinSecret("cVTTtWtqqiqouZfaNiDck2eYoT8FDyg82TsFBKhWEgnq8pa7LjHG")
key3_addr = P2PKHBitcoinAddress.from_pubkey(key3.pub)

key4 = CBitcoinSecret("cVcbvpStwtvL91yQWAzReREQHJe2gNb5x2VCDSnkmnngvMM5eKWK")
key4_addr = P2PKHBitcoinAddress.from_pubkey(key4.pub)

key5 = CBitcoinSecret("cT4RSXGDp7Fa7aMfFr7zaocNbGy7gW53MLwGsygV6dWfzHfwLHM1")
key5_addr = P2PKHBitcoinAddress.from_pubkey(key5.pub)

print(key1_addr)
print(key2_addr)
print(key3_addr)
print(key4_addr)
print(key5_addr)

# mmd27WqESsqtBAAp2XZAp9VWC4Qy8jJUnT
# mxpf6p8WE7tUmYoPZSwJ9HbTYARZo6SQFw
# mr5euUubdz2MBaP6CQJSjoFdyzfYju2ov8
# mshR5fsbimUp8hJ9JReRs5vLNVXnY1FJKn
# mn6na19twmjVicKvnkHpYypn8mJs6F5e1b
