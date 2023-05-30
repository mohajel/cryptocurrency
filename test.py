from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
from bitcoin.core import b2x, Hash
from utils import *
import struct
import time

bitcoin.SelectParams("mainnet") 
my_private_key = CBitcoinSecret("L4vB5fomsK8L95wQ7GFzvErYGht49JsCPJyJMHpB4xGM6xgi2jvG")
my_public_key = my_private_key.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)


print(my_private_key)
print(my_public_key)
print(my_address)