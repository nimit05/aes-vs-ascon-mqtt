import ascon
import os

KEY = os.urandom(16)   # 128-bit
NONCE = os.urandom(16) # 128-bit

def ascon_encrypt(plaintext: str) -> tuple:
    ciphertext = ascon.encrypt(KEY, NONCE, plaintext.encode(), b"")
    return ciphertext, NONCE

def ascon_decrypt(ciphertext: bytes, nonce: bytes) -> str:
    plaintext = ascon.decrypt(KEY, nonce, ciphertext, b"")
    return plaintext.decode()
