# import bitcoin.wallet
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *



bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = CBitcoinSecret("931cPqJ5igurei6mQSQYfte9buw3KGF6VERz9hDekukF5Dcwf23") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)
# destination_address = CBitcoinAddress('mvpwgfvoWc6Bv8R6f5h3JUYQnjesWNAKdZ') # Destination address (recipient of the money)

def P2PKH_scriptPubKey(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY, OP_CHECKSIG]
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

    txin_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)

def make_1to2_transaction(amount_to_send_1 , amount_to_send_2, txid_to_spend, utxo_index ,txout_scriptPubKey_1 ,txout_scriptPubKey_2):
    txout1 = create_txout(amount_to_send_1, txout_scriptPubKey_1)
    txout2 = create_txout(amount_to_send_2, txout_scriptPubKey_2)

    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig_2output(txin, txout1, txout2, txin_scriptPubKey)

    new_tx = create_1to2_signed_transaction(txin, txout1, txout2, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    amount_to_send_1 = 0.01
    amount_to_send_2 = 0.001
    # 8f69c1fb76d8a9113b9b88eaea421fc0f379c290b422576780ec0a798fe34ef9
    # eed80e568751fca412994d135a895fe681da886791333186c316b4c2e28f4162

    txid_to_spend = ('5e6c82a0afbf6618e9fff86cc2b2b6dcd10fb7ef10d1efb39b9079adcc46e2e2') # TxHash of UTXO
    utxo_index = 0 # UTXO index among transaction outputs
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_not_usable_scriptPubKey = P2PKH_return_scriptPubKey()
    txout_free_scriptPubKey = P2PKH_free_scriptPubKey()
    response = make_1to2_transaction(amount_to_send_1, amount_to_send_2, txid_to_spend, utxo_index, txout_not_usable_scriptPubKey, txout_free_scriptPubKey)

    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result

