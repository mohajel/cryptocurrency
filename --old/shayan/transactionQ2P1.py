import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *


bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("91csCMJdVymT5i1YuiPrWkqH9AqZdi2d22bU9oK5ircKYR9saPK")
first_person_private_key = bitcoin.wallet.CBitcoinSecret("923qXJ3XEP6Zp2CfDzxAug8rTVrt95Qyv8WKRNPsty7jhuhPNQr")
second_person_private_key = bitcoin.wallet.CBitcoinSecret("935Z9GS9MZGKcd2v6URnPivkW5F9XCt4CYsxe3jui9DYqyexoza")
third_person_private_key = bitcoin.wallet.CBitcoinSecret("92dhsHTLrWC7H8SmctgquXQRrW3c8zVAQAF3V3151GjSwaySDS6")
my_public_key = my_private_key.pub
first_person_public_key = first_person_private_key.pub
second_person_public_key = second_person_private_key.pub
third_person_public_key = third_person_private_key.pub

def P2PKH_txin_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def MultiSig_output_script():
    return [OP_2, first_person_public_key, second_person_public_key, third_person_public_key, OP_3, OP_CHECKMULTISIG]

def make_multisig_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_txin_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    amount_to_send = 0.005
    txid_to_spend = ('164b9de7920ad42eb57b4f0681f829d42512710ce73e7a921ca32ed31e75628b')
    utxo_index = 1
    ### make_transaction
    txout_scriptPubKey = MultiSig_output_script()
    response = make_multisig_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)