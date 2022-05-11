import binascii
import hashlib

with open('6 - 1 - Introduction (11 min).mp4', 'br') as f:
    file_bytes = f.read()

odd_block_len = len(file_bytes) % 1024

if odd_block_len != 0:
    last_block = file_bytes[-odd_block_len:]
    normal_block_bytes = file_bytes[:-odd_block_len]
else:
    last_block = file_bytes[-1024:]
    normal_block_bytes = file_bytes[:1024]

block_hash = hashlib.sha256(last_block).digest()

for i in range(len(normal_block_bytes) // 1024):
    start_byte = -1024 * (i + 1) 
    end_byte = -1024 * i
    if end_byte == 0:
        block_without_hash = normal_block_bytes[start_byte:]
    else:
        block_without_hash = normal_block_bytes[start_byte:end_byte]

    block = block_without_hash + block_hash

    block_hash = hashlib.sha256(block).digest()

print(binascii.hexlify(block_hash))
