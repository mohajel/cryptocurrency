import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x, Hash
from utils import *
import time,struct

def get_P2PKH_output_script(my_public_key):
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def get_my_public_key():
    bitcoin.SelectParams('mainnet')
    my_public_key = bitcoin.wallet.CBitcoinSecret('5JUUqpXwREFX5emdDCRS5dt7R6m1KxrvaUWjtUFzgo1VEPVUPLr').pub
    print('my address: ',bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key))
    return my_public_key

def get_target(bits):
    exponent = bits[2:4]
    coefficient = bits[4:]
    exponent2 = 8 * (int(exponent,16) - 3)
    target = int(coefficient, 16) * (2**exponent2)
    target = format(target, 'x')
    target_byte = bytes.fromhex(str(target).zfill(64))
    print('target: ', str(target).zfill(64)) # if we are smaller than 0x0001,we have 4 leading zeros
    return target_byte

def make_coinbase_transaction(base_amount_to_send, coinbase_txid_to_spend, coinbase_utxo_index,
        output_script, coinbase_script_sig):
    txin = create_txin(coinbase_txid_to_spend, coinbase_utxo_index)
    txout = create_txout(base_amount_to_send, output_script)
    tx = CMutableTransaction([txin], [txout])
    txin.scriptSig = coinbase_script_sig
    return tx

def get_merkle_root(coinbase_tx):
    coinbase_serialized = b2x(coinbase_tx.serialize())
    merkle_root = b2lx(coinbase_tx.GetTxid())
    print('block body: ', coinbase_serialized)
    print('merkle_root: ', merkle_root)
    return merkle_root,coinbase_serialized

def get_partial_header(version, last_block_hash, merkle_root, bits):
    time_now = int(time.time())
    return struct.pack("<L", version) + bytes.fromhex(last_block_hash)[::-1] + bytes.fromhex(merkle_root)[::-1] + struct.pack('<LL', time_now, int(bits, 16))

def mine_block(partial_header, target):
    nounce = 0
    while nounce <= 0xFFFFFFFF:
        header = partial_header + struct.pack('<L', nounce)
        block_hash = Hash(header)
        if block_hash[::-1] < target:
            print('Nounce found : ', nounce)
            return header, block_hash
        nounce += 1
    raise BaseException('Cannot find a suitable nounce to mine a block')

if __name__ == '__main__':
    print("what is the block number?")
    #n = 7493
    n = input()
    print("what is the block hash?")
    #hash: 000000000e07b8b1072caa57878b8943dc27fa398cbb57e7d45f4084d4773ca1
    last_block_hash = input()
    block_version = 2
    bits = '0x1f010000' #for first four bits zero
    base_amount_to_send = 6.25
    coinbase_txid_to_spend = (64*'0')
    coinbase_utxo_index = int('0xFFFFFFFF', 16)
    coinbase_hex_data = '810197493ShayanHamidiDehshali'.encode('utf-8').hex()
    print('coinbase hexadecimal data: ', coinbase_hex_data)
    output_script = get_P2PKH_output_script(get_my_public_key())
    coinbase_script_sig = CScript([int(coinbase_hex_data, 16).to_bytes(len(coinbase_hex_data)//2, 'big')])
    coinbase_tx = make_coinbase_transaction(base_amount_to_send, coinbase_txid_to_spend, coinbase_utxo_index,
        output_script, coinbase_script_sig)
    merkle_root,block_body = get_merkle_root(coinbase_tx)
    target = get_target(bits)
    partial_header = get_partial_header(block_version, last_block_hash, merkle_root, bits)
    header, block_hash = mine_block(partial_header, target)
    print('Block with hash ', b2lx(block_hash), ' created!')
    print('Block header: ', b2x(header))
    print('Block body: ', block_body)
