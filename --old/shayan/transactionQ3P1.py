import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

#address :mkjqy8YPQEZas2NFk5JADr4gb1JtDK6NQk
bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("93QEpDA2c9i3Zkk1q3cuAxTvsH1kbzijY63ky5VWGJtrkaXerMS") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub

def P2PKH_txin_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def get_redeem_script():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def make_P2SH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                redeem_script):
    txout = CMutableTxOut(amount_to_send*COIN, CScript(redeem_script).to_p2sh_scriptPubKey())
    txin_scriptPubKey = P2PKH_txin_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    amount_to_send = 0.011
    txid_to_spend = ('e6725ca280690a924b74aa2556e3ccb4fc56edfbcaace4bf3d490f59d7c724ac')
    utxo_index = 0

    redeem_script = get_redeem_script()
    response = make_P2SH_transaction(amount_to_send, txid_to_spend, utxo_index, redeem_script)
    print(response.status_code, response.reason)
    print(response.text)
