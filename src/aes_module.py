from Crypto.Cipher import AES
from config import AES_KEY, AES_NONCE
import os


def aes_encrypt(plaintext: str) -> tuple:
    cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=AES_NONCE)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return ciphertext, tag

def aes_decrypt(ciphertext: bytes, tag: bytes) -> str:
    cipher = AES.new(AES_KEY, AES.MODE_GCM, AES_NONCE, nonce=AES_NONCE)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext
