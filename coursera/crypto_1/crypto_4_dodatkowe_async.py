import asyncio
import binascii
import time

import aiohttp

HTTP_CLIENT = aiohttp.ClientSession()

@asyncio.coroutine
def decode_last_block(cipher_int, cipher_byte_length):
    block_guess = 0
    for block_byte in range(1,17):
        # 1 byte with value 1, 2 bytes with value 2, etc.
        oracle_mask = bytes([block_byte for _ in range(block_byte)])

        shift = 128 + ((block_byte - 1) * 8)
        # to xor with second to last ciphertext block
        oracle_mask_int = int.from_bytes(oracle_mask, 'big') << shift
        increment = 1 << shift
        
        with aiohttp.ClientSession() as client:
            tasks = []
            for i in range(256):
                guess = block_guess + (increment * i)
                #print('{:x}'.format(guess))
                tasks.append(asyncio.async(
                    check_guess(guess, cipher_int, oracle_mask_int, cipher_byte_length)
                ))
                
            done, _ = yield from asyncio.wait(tasks)
            try:
                block_guess = next(f.result() for f in done if f.result() >= 0)
            except StopIteration:
                raise(Exception("Couldn't find right pad for block byte {}".format(block_byte)))
    return int.to_bytes(guess >> 128, 16, 'big')

@asyncio.coroutine
def check_guess(guess, cipher_int, oracle_mask_int, cipher_byte_length):
    #print('{:x}'.format(guess))
    #print('{:x}'.format(oracle_mask_int))
    guess_cipher = cipher_int ^ guess ^ oracle_mask_int
    # we just sent the original ciphertext, we don't learn anything
    if guess_cipher == cipher_int:
        return -1 
    guess_cipher_hex = hex(guess_cipher)[2:]

    resp = yield from HTTP_CLIENT.get('http://crypto-class.appspot.com/po?er=' + guess_cipher_hex)
    resp.close()

    #print(resp.status)
    if resp.status in (200,404):
        print(hex(guess))
        return guess
    else:
        return -1

@asyncio.coroutine
def decipher():
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
    
    block = yield from decode_last_block(cipher_int, len(cipher))
    print(block)

    hax_time = time.perf_counter() - hax_start_time
    print('Haxed in {} seconds.'.format(hax_time))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(decipher())
