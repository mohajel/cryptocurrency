# In the Name of God

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


def P2PKH_locking_script(public_key):
    return [OP_DUP, OP_HASH160, Hash160(public_key), OP_EQUALVERIFY, OP_CHECKSIG]


def make_coinbase_transaction(
    reward_amount, txin_address, txin_index, output_script, coinbase_bytes_data
):
    txin = create_txin(txin_address, txin_index)
    txout = create_txout(block_reward, output_script)
    tx = CMutableTransaction([txin], [txout])
    txin.scriptSig = coinbase_bytes_data
    return tx


def calculate_merkle_root(coinbase_tx):
    return Hash(coinbase_tx.serialize())


def create_initial_header(prev_block_hash, merkle_root, mine_target: int, version):
    version_bytes = struct.pack("<I", version)
    prev_block_hash_bytes = bytes.fromhex(prev_block_hash)[::-1]
    merkle_root_bytes = merkle_root[::-1]
    timestamp_bytes = struct.pack("<I", int(time.time()))
    target_bytes = mine_target.to_bytes(64, "big")

    return (
        version_bytes
        + prev_block_hash_bytes
        + merkle_root_bytes
        + timestamp_bytes
        + target_bytes
    )


def calculate_mine_target(leading_zeroes_in_bits):
    return 2 ** (256 - leading_zeroes_in_bits)


def mine_next_block(initial_header, target_in_bytes):
    nonce = 0
    while nonce < 0xFFFFFFFF:
        header = initial_header + struct.pack("<I", nonce)
        block_hash = Hash(header)
        if block_hash < target_in_bytes:
            print("Nonce found:", nonce)
            return header, block_hash
        nonce += 1


def print_transaction_info(coinbase_tx: CMutableTransaction):
    print("transaction_out:\n{\n   Input:", coinbase_tx.vin)
    print("   Output:", coinbase_tx.vout)
    print("}")


def print_mining_info(
    coinbase_tx: CMutableTransaction,
    prev_block_number,
    prev_block_hash,
    block_reward,
    coinbase_data,
    coinbase_hex_data,
    block_hash,
    header,
    block_body,
):
    print("Previous Block Number: ", prev_block_number)
    print("Previous Block Hash: ", prev_block_hash)
    print("Mining reward:", block_reward)
    print("Coinbase data: ", coinbase_data)
    print("Coinbase hex data: ", coinbase_hex_data)
    print_transaction_info(coinbase_tx)
    print("Block hash:", b2x(block_hash))
    print("Block header:", b2x(header))
    print("Block Body in hex:", b2x(block_body))


if __name__ == "__main__":
    prev_block_number = 9483
    prev_block_hash = "00000000cb0356066b1f8d2482c4747e8da716bf355b71f88fad0b3c3bdd62d8"
    block_reward = 3.125
    coinbase_data = "810199483MohammadMohajelSadegi"
    coinbase_hex_data = coinbase_data.encode("utf-8").hex()
    coinbase_txin = 64 * "0"  # Ask why not 32
    coinbase_utxo_index = 0xFFFFFFFF
    output_script = P2PKH_locking_script(my_public_key)
    coinbase_scriptSig = CScript([bytes.fromhex(coinbase_hex_data)])
    coinbase_tx = make_coinbase_transaction(
        block_reward,
        coinbase_txin,
        coinbase_utxo_index,
        output_script,
        coinbase_scriptSig,
    )
    merkle_root = calculate_merkle_root(coinbase_tx)
    target = calculate_mine_target(16)
    initial_header = create_initial_header(
        prev_block_hash, merkle_root, target, version=1
    )
    header, block_hash = mine_next_block(initial_header, target.to_bytes(32, "big"))
    block_body = header + coinbase_tx.serialize()
    print_mining_info(
        coinbase_tx,
        prev_block_number,
        prev_block_hash,
        block_reward,
        coinbase_data,
        coinbase_hex_data,
        block_hash,
        header,
        block_body,
    )
