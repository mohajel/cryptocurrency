# import bitcoin.wallet
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *



output_address1 = "miipFUHTcVny29mPgsobSEAtS4sAXazFBv"
output_address2 = "mjLRVq15q6Qwpn4fQyzSLsjzYCq6aLRmjs"
output_address3 = "mhPavQtru2CbGb3acy14ArLC8w95MRBSvw"

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
first_user_prk = CBitcoinSecret("93R6C1uspBV9RFtNXjc1oEFZXA494HMjZBNUpKueZhPx2iFVAWG")
second_user_prk = CBitcoinSecret("92h8FzaffymGV8JZgYtTwNmeK2QNVXvKEms7yVtDUoyRtHpG2YN")
third_user_prk = CBitcoinSecret("91rEuvZai6xBjbSAX4qdL4tWBj8ANktypVhKkjwQciUfB71noZx")

first_user_pub = first_user_prk.pub
second_user_pub = second_user_prk.pub
third_user_pub = third_user_prk.pub

my_private_key = CBitcoinSecret("93R6C1uspBV9RFtNXjc1oEFZXA494HMjZBNUpKueZhPx2iFVAWG") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)
# destination_address = CBitcoinAddress('mvpwgfvoWc6Bv8R6f5h3JUYQnjesWNAKdZ') # Destination address (recipient of the money)





def P2PKH_scriptPubKey(public_key):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##
    return [OP_DUP, OP_HASH160, Hash160(public_key), OP_EQUALVERIFY, OP_CHECKSIG]
    ######################################################################

def multisig_locking_script(public_key_1, public_key_2, public_key_3):
    return [OP_2 , public_key_1, public_key_2, public_key_3, OP_3, OP_CHECKMULTISIG]

def multisig_unlocking_script(txin, txout, txin_scriptPubKey, private_key1, private_key2):
    first_user_signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, private_key1)
    second_user_signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, private_key2)
    return [OP_0, first_user_signature, second_user_signature]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    ######################################################################
    ## Fill out the operations for P2PKH scriptSig                      ##
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key] #Fill this section
    ######################################################################


def make_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)

def make_multisig_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = multisig_locking_script(first_user_pub, second_user_pub, third_user_pub)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = multisig_unlocking_script(txin, txout, txin_scriptPubKey, second_user_prk, third_user_prk)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    ######################################################################
    amount_to_send = 0.008

    txid_to_spend = ('4ad64a8fc862f43495af8bd713f689eb18450d77e6b23fcd5188cc99b02dbea9') # TxHash of UTXO
    utxo_index = 0 # UTXO index among transaction outputs
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    response = make_multisig_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)



    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result

