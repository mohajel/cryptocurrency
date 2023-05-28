import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

#address: mkjqy8YPQEZas2NFk5JADr4gb1JtDK6NQk
#segwit_address: tb1qm83uu3xg7h8s4f026f9n9c8pc0vkpq3hktn9xj
#segwit_private_key_WIF: cSWzxfnTLKAPs5rnVVzTS7fCe68c3kjASg3Ab3T37hf9qbhnY2jx
bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("93QEpDA2c9i3Zkk1q3cuAxTvsH1kbzijY63ky5VWGJtrkaXerMS")
my_public_key = my_private_key.pub
generated_segwit_address = bitcoin.wallet.P2WPKHBitcoinAddress('tb1qm83uu3xg7h8s4f026f9n9c8pc0vkpq3hktn9xj')

def P2PKH_txin_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def P2WPKH_output_script():
    return generated_segwit_address.to_scriptPubKey()

def make_P2WPKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                output_script):
    txout = create_txout(amount_to_send, output_script)
    txin_scriptPubKey = P2PKH_txin_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    amount_to_send = 0.006
    txid_to_spend = ('6616888e5b966cd38a3dd9ea28617d6a50ae1c6b975539a0a685e629a397e0c4')
    utxo_index = 0

    output_script = P2WPKH_output_script()
    response = make_P2WPKH_transaction(amount_to_send, txid_to_spend, utxo_index, output_script)
    print(response.status_code, response.reason)
    print(response.text)

