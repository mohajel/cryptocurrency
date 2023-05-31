from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress
import bitcoin
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils_temp import *

bitcoin.SelectParams("testnet")
my_private_key = CBitcoinSecret("cTkSSMQbC9pxYKf1iRPTZ69pjcWP1bS2vAGhDMPV32izxKXtiU6u")
my_public_key = my_private_key.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)


def make_1to2_transaction(amount_to_send_1 , amount_to_send_2, txid_to_spend, utxo_index ,txout_scriptPubKey_1 ,txout_scriptPubKey_2):
    txout1 = create_txout(amount_to_send_1, txout_scriptPubKey_1)
    txout2 = create_txout(amount_to_send_2, txout_scriptPubKey_2)

    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig_2output(txin, txout1, txout2, txin_scriptPubKey, my_private_key, my_public_key)

    new_tx = create_1to2_signed_transaction(txin, txout1, txout2, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    amount_to_send_1 = 0.001
    amount_to_send_2 = 0.01

    txid_to_spend = ('2bf293def1f9cd22601c592ed3a53438a04d923789057c37f7a6e52ba8b347b1')
    utxo_index = 1

    txout_not_usable_scriptPubKey = P2PKH_return_scriptPubKey()
    txout_free_scriptPubKey = P2PKH_free_scriptPubKey()
    response = make_1to2_transaction(amount_to_send_1, amount_to_send_2, txid_to_spend, utxo_index, txout_not_usable_scriptPubKey, txout_free_scriptPubKey)

    print(response.status_code, response.reason)
    print(response.text)

