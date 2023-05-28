import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

#address: mkjqy8YPQEZas2NFk5JADr4gb1JtDK6NQk
#segwit_address: tb1qm83uu3xg7h8s4f026f9n9c8pc0vkpq3hktn9xj
#segwit_private_key_WIF: cSWzxfnTLKAPs5rnVVzTS7fCe68c3kjASg3Ab3T37hf9qbhnY2jx
bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("93QEpDA2c9i3Zkk1q3cuAxTvsH1kbzijY63ky5VWGJtrkaXerMS")
my_public_key = my_private_key.pub
segwit_address = bitcoin.wallet.P2WPKHBitcoinAddress('tb1qm83uu3xg7h8s4f026f9n9c8pc0vkpq3hktn9xj')
segwit_private_key = bitcoin.wallet.CBitcoinSecret("cSWzxfnTLKAPs5rnVVzTS7fCe68c3kjASg3Ab3T37hf9qbhnY2jx")
segwit_public_key = segwit_private_key.pub

def P2PKH_txout_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PWKH_witness(txin, txout, redeem_script, private_key, public_key, amount_spent):
    signature = create_witness(txin, txout, redeem_script, private_key, amount_spent)
    return [signature, public_key]

def P2WPKH_redeem_script():
    return segwit_address.to_redeemScript()

def spend_P2WPKH_transaction(amount_to_send, txid_to_spend, utxo_index, output_script, amount_spent):
    txout = create_txout(amount_to_send, output_script)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_redeem_script = P2WPKH_redeem_script()
    witness = P2PWKH_witness(txin, txout, txin_redeem_script, 
        segwit_private_key, segwit_public_key, amount_spent)
    new_tx = create_transaction_with_witness(txin, txout, witness)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    amount_to_send = 0.002
    txid_to_spend = ('e124e304fa79919464a15505669bd44b64b401d49fa2b4f9dd10eb8bdc570952')
    utxo_index = 0
    amount_spent = 0.006

    output_script = P2PKH_txout_scriptPubKey()
    response = spend_P2WPKH_transaction(amount_to_send, txid_to_spend, utxo_index, output_script, amount_spent)
    print(response.status_code, response.reason)
    print(response.text)

#transaction_hash: 0db597e00a0954cf7e64637dabe723bd1e81b7d936efd863ebdf4012672b88f1