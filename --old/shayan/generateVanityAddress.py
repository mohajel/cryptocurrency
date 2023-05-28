import generateAddress
import base58   

def find_vanity_address(first_bytes):
    if (len(first_bytes) > 3):
        return "error","Three first characters(except n/m),at most, must be entered!"
    try:
        base58.b58decode(first_bytes)
    except:
        return "error","Your characters are not in Base58 format!"
    _,_, produced_private_key, produced_address = generateAddress.produce_keys()
    while produced_address[1:(len(first_bytes) + 1)] != first_bytes:
        _,_, produced_private_key, produced_address = generateAddress.produce_keys()
    return produced_private_key, produced_address        

first_bytes = input()
private_key, address = find_vanity_address(first_bytes)
if private_key == "error":
    print(address)
else:
    print(private_key.decode("utf-8"))
    print(address.decode("utf-8"))