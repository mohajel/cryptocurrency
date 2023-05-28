import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

#txid: 4db0a206c937f23e79c65d6ac9695a08c64d3e0067a238e41d3a371362800a0a
#my Address: mxCCif7LNNAd3veVkV9WmR2sbwkMngpMiA
bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("91csCMJdVymT5i1YuiPrWkqH9AqZdi2d22bU9oK5ircKYR9saPK")
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def get_txin_scriptPubKey():
    return [OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = get_txin_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    amount_to_send = 0.00005
    txid_to_spend = ('4db0a206c937f23e79c65d6ac9695a08c64d3e0067a238e41d3a371362800a0a') # TxHash of UTXO
    utxo_index = 1

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = P2PKH_scriptPubKey(my_address)
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result

#transaction spent: 13c85b6ac7fc914883b308693da2cf0810be1491686e8953e276d5decfd5aafd