from cryptography.fernet import Fernet
from faker import Faker

key = Fernet.generate_key()
f = Fernet(key)

text = Faker().text()
print('Text to encrypt:', text, '\n')

token = f.encrypt(text.encode())
print('Encrypted text:', token, '\n')

decrypted = f.decrypt(token)
print('Decrypted text:', decrypted)
