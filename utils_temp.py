import hashlib
import secrets
import base58
import requests

from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import *
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH


def create_random_private_key_hex():
    # Generate a random 256-bit number
    private_key_int = secrets.randbits(256)
    # Convert the number to a hexadecimal string
    private_key_hex = hex(private_key_int)[2:].zfill(64)
    return private_key_hex

def hex_to_wif(hex, prefix = "ef", compressed = True):
    compressed_hex = ""
    if compressed:
        compressed_hex = "01"
    hex = prefix + hex + compressed_hex 
    bytes_string = bytes.fromhex(hex)
    checksum = hashlib.sha256( hashlib.sha256(bytes_string).digest()).digest()[:4]
    hex = hex + checksum.hex()

    return base58.b58encode(bytes.fromhex(hex)).decode()

# locking script
def P2PKH_scriptPubKey(address): 
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]

# Unlocking script
def P2PKH_scriptSig(txin, txout, txin_scriptPubKey, private_key, public_key):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, private_key)
    return [signature, public_key] 

def P2PKH_scriptSig_2output(txin, txout1, txout2, txin_scriptyPubKey, private_key, public_key):
    signature = create_OP_CHECKMULTISIG_signature(txin, txout1, txout2, txin_scriptyPubKey, private_key)
    return [signature, public_key]

def P2PKH_return_scriptPubKey():
    return [OP_RETURN]

def P2PKH_free_scriptPubKey():
    return [OP_CHECKSIG]

def make_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey, address, pri, pub):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey, pri, pub)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)

def send_from_custom_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        txin_scriptPubKey, txin_scriptSig, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin = create_txin(txid_to_spend, utxo_index)
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)
    return broadcast_transaction(new_tx)


def create_txin(txid, utxo_index):
    return CMutableTxIn(COutPoint(lx(txid), utxo_index))


def create_txout(amount, scriptPubKey):
    return CMutableTxOut(amount*COIN, CScript(scriptPubKey))


def create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, seckey):
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(CScript(txin_scriptPubKey), tx,
                            0, SIGHASH_ALL)
    sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
    return sig

def create_OP_CHECKMULTISIG_signature(txin, txout1, txout2, txin_scriptPubKey, seckey):
    tx = CMutableTransaction([txin], [txout1, txout2])
    sighash = SignatureHash(CScript(txin_scriptPubKey), tx,
                            0, SIGHASH_ALL)
    sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
    return sig

def create_signed_transaction(txin, txout, txin_scriptPubKey,
                              txin_scriptSig):
    tx = CMutableTransaction([txin], [txout])
    txin.scriptSig = CScript(txin_scriptSig)
    VerifyScript(txin.scriptSig, CScript(txin_scriptPubKey),
                 tx, 0, (SCRIPT_VERIFY_P2SH,))
    return tx

def create_1to2_signed_transaction(txin, txout1, txout2, txin_scriptPubKey,
                              txin_scriptSig):
    tx = CMutableTransaction([txin] , [txout1, txout2], witness=None)
    txin.scriptSig = CScript(txin_scriptSig)
    VerifyScript(txin.scriptSig, CScript(txin_scriptPubKey),
                 tx, 0, (SCRIPT_VERIFY_P2SH,))
    return tx

def broadcast_transaction(tx):
    raw_transaction = b2x(tx.serialize())
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    return requests.post(
        'https://api.blockcypher.com/v1/btc/test3/txs/push',
        # 'https://sochain.com/testnet/btc/test3/txs/push',
        headers=headers,
        data='{"tx": "%s"}' % raw_transaction)

# https://sochain.com/testnet/btc