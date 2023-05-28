import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *
from transactionQ2P1 import *

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("91csCMJdVymT5i1YuiPrWkqH9AqZdi2d22bU9oK5ircKYR9saPK") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub

def P2PKH_output_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key), OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    first_person_signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, first_person_private_key)
    second_person_signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, second_person_private_key)

    return [OP_0, first_person_signature, second_person_signature]

def make_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptPubKey = MultiSig_output_script()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    amount_to_send = 0.002
    txid_to_spend = ('7c0465511ea565ba6242b162a61f964762398a54ca07bbbfa257a70b4c0f611d')
    utxo_index = 0
    txout_scriptPubKey = P2PKH_output_scriptPubKey()
    response = make_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)

#transaction_hash:5a085b74e174de7de003ff695bb2376ea421f386be6f5a52a439f7861fd97ec6
