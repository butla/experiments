import binascii
import time

import requests

def decode_last_block(cipher_int):
    guess = 0
    for block_byte in range(1,17):
        # 1 byte with value 1, 2 bytes with value 2, etc.
        oracle_mask = bytes([block_byte for _ in range(block_byte)])

        shift = 128 + ((block_byte - 1) * 8)
        # to xor with second to last ciphertext block
        oracle_mask_int = int.from_bytes(oracle_mask, 'big') << shift
        increment = 1 << shift

        for i in range(256):
            print('{:x}'.format(guess))
            #print('{:x}'.format(oracle_mask_int))
            guess_cipher = cipher_int ^ guess ^ oracle_mask_int
            # we just sent the original ciphertext, we don't learn anything
            if guess_cipher == cipher_int:
                guess += increment
                continue
            
            guess_cipher_bytes = int.to_bytes(guess_cipher, len(cipher), 'big')
            guess_cipher_hex = binascii.hexlify(guess_cipher_bytes)
            #print(guess_cipher_hex)

            resp = requests.get(b'http://crypto-class.appspot.com/po?er=' + guess_cipher_hex)

            #print(resp.status_code)
            if resp.status_code != 403:
                print('Byte {} is {}'.format(block_byte, i))
                break

            guess += increment # guess will go up to 255 (shifted by the right amount)
        else:
            raise(Exception("Couldn't find right pad for block byte {}".format(block_byte)))
    return int.to_bytes(guess >> 128, 16, 'big')


if __name__ == '__main__':
    cipher_hex = b'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
    cipher = binascii.unhexlify(cipher_hex)

    # Cipher is 64 bytes long, so 4 128 bit blocks, including IV.
    # We're going to be guessing by xoring IV, c0, and c1.
    # Block c2 will not be tampered with.
    # Max 1 block can be filled with padding.

    # Jaki bedzie czas synchroniczny, sekwencyjny, a jaki, jak dla każdego bajtu
    # wyślemy rownolegle przez aiohttp?

    hax_start_time = time.perf_counter()

    cipher_int = int.from_bytes(cipher, 'big')
    
    print(decode_last_block(cipher_int))

    hax_time = time.perf_counter() - hax_start_time
    print('Haxed in {} seconds.'.format(hax_time))
