import requests
import hashlib as hash
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160, CTxInWitness, CTxWitness
from bitcoin.core.script import *
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH

def Sha256(unhashed_data):
    digester = hash.new("sha256")
    digester.update(unhashed_data)
    return digester.digest()

def RipeMD160(unhashed_data):
    digester = hash.new("ripemd160")
    digester.update(unhashed_data)
    return digester.digest()

def calculate_checksum(key):
    hashed_data = Sha256(Sha256(key))
    return hashed_data[:4]

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

def create_OP_CHECKSIG_signature_two_outputs(txin, first_txout, second_txout, txin_scriptPubKey, seckey):
    tx = CMutableTransaction([txin], [first_txout, second_txout])
    sighash = SignatureHash(CScript(txin_scriptPubKey), tx,
                            0, SIGHASH_ALL)
    sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
    return sig

def create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, seckey):
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(CScript(txin_scriptPubKey), tx,
                            0, SIGHASH_ALL)
    sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
    return sig

def create_witness(txin, txout, redeem_script, seckey, amount_spent):
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(redeem_script, tx, 0, 
        SIGHASH_ALL, amount=int(amount_spent*COIN), sigversion=SIGVERSION_WITNESS_V0)
    sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
    return sig

def create_signed_transaction_two_outputs(txin, first_txout, second_txout, txin_scriptPubKey,
                              txin_scriptSig):
    tx = CMutableTransaction([txin], [first_txout, second_txout])
    txin.scriptSig = CScript(txin_scriptSig)
    VerifyScript(txin.scriptSig, CScript(txin_scriptPubKey),
                 tx, 0, (SCRIPT_VERIFY_P2SH,))
    return tx

def create_signed_transaction(txin, txout, txin_scriptPubKey,
                              txin_scriptSig):
    tx = CMutableTransaction([txin], [txout])
    txin.scriptSig = CScript(txin_scriptSig)
    VerifyScript(txin.scriptSig, CScript(txin_scriptPubKey),
                 tx, 0, (SCRIPT_VERIFY_P2SH,))
    return tx

def create_transaction_with_witness(txin, txout, txin_witness):
    tx = CMutableTransaction([txin], [txout])
    ctxinwitnesses = [CTxInWitness(CScriptWitness(txin_witness))]
    tx.wit = CTxWitness(ctxinwitnesses)
    return tx


def broadcast_transaction(tx):
    raw_transaction = b2x(tx.serialize())
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    return requests.post(
        'https://api.blockcypher.com/v1/btc/test3/txs/push',
        headers=headers,
        data='{"tx": "%s"}' % raw_transaction)
