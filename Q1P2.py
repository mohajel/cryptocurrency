#OK

from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *



bitcoin.SelectParams("testnet")
my_private_key = CBitcoinSecret("cNuJHQPJ417DT55KgNbvVNzKXXLX4UFxoRb1gb9sRx1Ga9oxaVuK") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)

def P2PKH_scriptPubKey(public_key):
    return [OP_DUP, OP_HASH160, Hash160(public_key), OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def P2PKH_scriptSig_2output(txin, txout1, txout2, txin_scriptyPubKey):
    signature = create_OP_CHECKMULTISIG_signature(txin, txout1, txout2, txin_scriptyPubKey, my_private_key)
    return [signature, my_public_key]

def P2PKH_return_scriptPubKey():
    return [OP_RETURN]

def P2PKH_free_scriptPubKey():
    return [OP_CHECKSIG]

def make_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_free_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amount_to_send = 0.005

    txid_to_spend = ('221a9452c99937c241acce0bcefbd3de4b26e4eecf897bc6ab8625999ec8f269') # TxHash of UTXO
    utxo_index = 1
    txout_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    response = make_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)

    print(response.status_code, response.reason)
    print(response.text)
