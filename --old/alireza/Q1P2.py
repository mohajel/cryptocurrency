# import bitcoin.wallet
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *



bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = CBitcoinSecret("93S78wP3T666D8wLtccQ79bsys631vSR64TMLKVishP6wG9m8Yp") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)
# destination_address = CBitcoinAddress('mvpwgfvoWc6Bv8R6f5h3JUYQnjesWNAKdZ') # Destination address (recipient of the money)

def P2PKH_scriptPubKey(public_key):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##
    return [OP_DUP, OP_HASH160, Hash160(public_key), OP_EQUALVERIFY, OP_CHECKSIG]
    ######################################################################

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    ######################################################################
    ## Fill out the operations for P2PKH scriptSig                      ##
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key] #Fill this section
    ######################################################################

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
    ######################################################################
    amount_to_send = 0.0009

    txid_to_spend = ('717708b1bb42a25f349bdd98eaa1beda361bce4a900f1c97e6cf5158f5860fed') # TxHash of UTXO
    utxo_index = 1 # UTXO index among transaction outputs
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    response = make_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)

    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result

