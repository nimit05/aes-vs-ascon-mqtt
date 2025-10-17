import ascon
import os
from config import ASCON_KEY, ASCON_NONCE

def ascon_encrypt(plaintext: str) -> tuple:
    ciphertext = ascon.encrypt(ASCON_KEY, ASCON_NONCE, plaintext, b"")
    return ciphertext, ASCON_NONCE

def ascon_decrypt(ciphertext: bytes) -> str:
    plaintext = ascon.decrypt(ASCON_KEY, ASCON_NONCE, ciphertext, b"")
    return plaintext.decode()
