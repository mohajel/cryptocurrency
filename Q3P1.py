# In the Name of God

from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
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

# mmd27WqESsqtBAAp2XZAp9VWC4Qy8jJUnT
# mxpf6p8WE7tUmYoPZSwJ9HbTYARZo6SQFw
# mr5euUubdz2MBaP6CQJSjoFdyzfYju2ov8
# mshR5fsbimUp8hJ9JReRs5vLNVXnY1FJKn
# mn6na19twmjVicKvnkHpYypn8mJs6F5e1b

my_private_key = key3
my_public_key = key3.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)


def customized_locking_script(sum_nums: bytes, sub_nums: bytes):
    return [
        OP_2DUP,
        OP_ADD,
        OP_HASH160,
        Hash160(sum_nums),
        OP_EQUALVERIFY,
        OP_SUB,
        OP_HASH160,
        Hash160(sub_nums),
        OP_EQUAL,
    ]


def customized_unlocking_script(prime_num1: bytes, prime_num2: bytes):
    return [prime_num1, prime_num2]


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(
        txin, txout, txin_scriptPubKey, my_private_key
    )
    return [signature, my_public_key]


def P2PKH_scriptPubKey(public_key):
    return [OP_DUP, OP_HASH160, Hash160(public_key), OP_EQUALVERIFY, OP_CHECKSIG]


def make_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == "__main__":
    amount_to_send = 0.0064
    txid_to_spend = "bfd6a5f51273842a0c8134be35a867db58b8afae75e568d0f12cfd8b59475323"  # TxHash of UTXO
    utxo_index = 0

    number_1 = 91
    number_2 = 23
    sum = number_1 + number_2
    sub = number_1 - number_2

    sum_bytes = sum.to_bytes(1, "little")
    sub_bytes = sub.to_bytes(1, "little")

    txout_scriptPubKey = customized_locking_script(sum_bytes, sub_bytes)
    response = make_transaction(
        amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey
    )

    print(response.status_code, response.reason)
    print(response.text)
