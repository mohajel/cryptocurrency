# import bitcoin.wallet
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *



output_address1 = "mjLRVq15q6Qwpn4fQyzSLsjzYCq6aLRmjs"

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = CBitcoinSecret("92h8FzaffymGV8JZgYtTwNmeK2QNVXvKEms7yVtDUoyRtHpG2YN") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)
# destination_address = CBitcoinAddress('mvpwgfvoWc6Bv8R6f5h3JUYQnjesWNAKdZ') # Destination address (recipient of the money)


def customized_locking_script(sum_nums:bytes, sub_nums:bytes):
    return [OP_2DUP, OP_ADD, OP_HASH160, Hash160(sum_nums), OP_EQUALVERIFY, OP_SUB, OP_HASH160, Hash160(sub_nums), OP_EQUAL]
    # return [OP_2DUP, OP_ADD, sum_nums, OP_EQUALVERIFY, OP_SUB, sub_nums, OP_EQUAL]

def customized_unlocking_script(prime_num1:bytes, prime_num2:bytes):
    return [prime_num1, prime_num2]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    ######################################################################
    ## Fill out the operations for P2PKH scriptSig                      ##
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key] #Fill this section
    ######################################################################

def P2PKH_scriptPubKey(public_key):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##
    return [OP_DUP, OP_HASH160, Hash160(public_key), OP_EQUALVERIFY, OP_CHECKSIG]
    ######################################################################


def make_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)




if __name__ == '__main__':
    ######################################################################
    amount_to_send = 0.0193

    txid_to_spend = ('66c465d841577e7a84f56c5f79e38a24465088e73085852af6bb230a6b57f123') # TxHash of UTXO
    utxo_index = 1 # UTXO index among transaction outputs
    ######################################################################
    prime_num1 = 89
    prime_num2 = 13
    sum = prime_num1 + prime_num2
    sub = prime_num1 - prime_num2
    ######################################################################
    prime_num1_bytes = prime_num1.to_bytes(1, 'little')
    prime_num2_bytes = prime_num2.to_bytes(1, 'little')
    sum_bytes = sum.to_bytes(1, 'little')
    sub_bytes = sub.to_bytes(1, 'little')

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = customized_locking_script(sum_bytes, sub_bytes)
    response = make_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)

    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result

