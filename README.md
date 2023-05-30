# In the Name of God

Mohammad Mohajel Sadegi - 810199483

# Phase 1:

In this phase, we are generating bitcoin testnet address.
First we create a random 256 bit private key and after that we do following:

    Use secp256k1 elliptic curve to generate public key from private key
    Hash the public key using SHA-256
    Hash the result again using RIPEMD-160
    Add version byte (0x00 for mainnet, 0x6f for testnet) to the RIPEMD-160 hash
    Compute checksum by hashing the version + RIPEMD-160 hash twice and taking the first 4 bytes
    Concatenate the version + RIPEMD-160 hash + checksum
    Encode the result using Base58Check encoding

After that we generate this random private keys repeatedly to find our desired vanity address

    A vanity address in Bitcoin is a custom Bitcoin address that contains specific chosen characters, such as a person's name or a specific phrase. While all Bitcoin addresses are technically random strings of numbers and letters, a vanity address is generated in such a way as to include a desired string of characters.

    Generating a vanity address can be a time-consuming process, as it requires repeatedly generating new addresses until one is found that meets the desired criteria. There are various tools available that can help facilitate the generation of vanity addresses, such as Vanitygen and VanitySearch.

    It is worth noting that while vanity addresses can be fun and personalized, they do not offer any additional security or privacy benefits over randomly generated addresses. In fact, using a vanity address could potentially make it easier for a malicious actor to determine the private key associated with that address, since the custom string of characters could provide additional clues about the key. Therefore, it is important to exercise caution and use best practices when generating and using Bitcoin addresses, regardless of whether they are vanity addresses or not.

You can find results below:
![test1](./images/q1.p1.png)

And to make sure our address is correct:
![test1](./images/q1.p2.png)