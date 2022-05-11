import asyncio
import binascii
import time

import aiohttp

HTTP_CLIENT = aiohttp.ClientSession()

BLOCK_SIZE = 16 

# TODO finding the actual padding of plaintext needs to be handled somehow

@asyncio.coroutine
def decode_last_block(cipher_int):
    # hack for the last message block
    #block_guess = 0x090909090909090909 << (BLOCK_SIZE*8)
    #for block_byte in range(10, BLOCK_SIZE+1):
    
    block_guess = 0
    for block_byte in range(1, BLOCK_SIZE+1):
        # 1 byte with value 1, 2 bytes with value 2, etc.
        oracle_mask = bytes([block_byte for _ in range(block_byte)])

        # to xor with second to last ciphertext block
        oracle_mask_int = int.from_bytes(oracle_mask, 'big') << (BLOCK_SIZE*8)
        shift = (BLOCK_SIZE*8) + ((block_byte - 1) * 8)
        increment = 1 << shift
        #print(shift)
        #print('{:x}'.format(increment))
        #print('{:x}'.format(cipher_int))
        #print('{:x}'.format(oracle_mask_int))
        
        tasks = []
        for i in range(256):
            guess = block_guess + (increment * i)
            #print('{:x}'.format(guess))
            tasks.append(asyncio.async(
                check_guess(guess, cipher_int, oracle_mask_int)
            ))
            
        done, _ = yield from asyncio.wait(tasks)
        try:
            block_guess = next(f.result() for f in done if f.result() >= 0)
        except StopIteration:
            raise(Exception("Couldn't find right pad for block byte {}".format(block_byte)))
    return int.to_bytes(guess >> (BLOCK_SIZE * 8), BLOCK_SIZE, 'big')


@asyncio.coroutine
def check_guess(guess, cipher_int, oracle_mask_int):
    guess_cipher = cipher_int ^ guess ^ oracle_mask_int
    # we just sent the original ciphertext, we don't learn anything
    if guess_cipher == cipher_int:
        return -1 
    guess_cipher_hex = hex(guess_cipher)[2:]
    #print(guess_cipher_hex)

    for _ in range(5):
        try:
            resp = yield from HTTP_CLIENT.get('http://crypto-class.appspot.com/po?er=' + guess_cipher_hex)
            resp.close()
            break
        except:
            print('get error')
    else:
        Exception("Just can't send")


    #print(resp.status)
    if resp.status in (200,404):
        print('Guessed!', hex(guess))
        return guess
    else:
        if resp.status != 403:
            print(resp.status)
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

    while True:
        # TODO last block is "sifrage", let's skip it,
        # we wouldn't need to if I implemented some sensible way
        # of finding out the plaintext padding
        cipher = cipher[:-16]
        if not cipher:
            break
        cipher_int = int.from_bytes(cipher, 'big')

        block = yield from decode_last_block(cipher_int)
        print(block)

    hax_time = time.perf_counter() - hax_start_time
    print('Haxed in {} seconds.'.format(hax_time))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(decipher())
