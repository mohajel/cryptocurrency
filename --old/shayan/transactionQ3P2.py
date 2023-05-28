import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

#address :mrpUc9LWpNKQAyHDd4RbZg6tsksmgDdVG2
bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("93QEpDA2c9i3Zkk1q3cuAxTvsH1kbzijY63ky5VWGJtrkaXerMS") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub

def P2SH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key, CScript([OP_DUP, OP_HASH160, Hash160(my_public_key), OP_EQUALVERIFY, OP_CHECKSIG])]

def txin_hashed_redeem_script():
    return CScript(P2PKH_txout_scriptPubKey()).to_p2sh_scriptPubKey()

def P2PKH_txout_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def spend_P2SH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptPubKey = txin_hashed_redeem_script()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2SH_scriptSig(txin, txout, P2PKH_txout_scriptPubKey())
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    amount_to_send = 0.009
    txid_to_spend = ('ab3e5019fac4633f0270381d508280e0b25f2535b8fdd5b58ab800fda47d9c03')
    utxo_index = 0
    txout_scriptPubKey = P2PKH_txout_scriptPubKey()
    response = spend_P2SH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)

#transaction_hash_spent: 6616888e5b966cd38a3dd9ea28617d6a50ae1c6b975539a0a685e629a397e0c4
