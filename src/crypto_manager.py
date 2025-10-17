import ascon
from Crypto.Cipher import AES
from config import AES_KEY, AES_NONCE, ASCON_KEY, ASCON_NONCE
import base64

ALGO_AES = "AES"
ALGO_ASCON = "ASCON"

def encrypt(plaintext: bytes, algo: str):
    if algo == ALGO_AES:
        cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=AES_NONCE)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        # Encode both as Base64 for safe MQTT transmission
        return base64.b64encode(ciphertext), base64.b64encode(tag)
    
    elif algo == ALGO_ASCON:
        ciphertext = ascon.encrypt(ASCON_KEY, ASCON_NONCE, b"", plaintext, variant="Ascon-128")
        # Base64 encode ciphertext
        return base64.b64encode(ciphertext), None
    
    else:
        raise ValueError(f"Unsupported algorithm: {algo}")


def decrypt(ciphertext_b64: bytes, algo: str, tag_b64: bytes = None) -> bytes:
    ciphertext = base64.b64decode(ciphertext_b64)
    if tag_b64:
        tag = base64.b64decode(tag_b64)
    else:
        tag = None

    if algo == ALGO_AES:
        cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=AES_NONCE)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext
    
    elif algo == ALGO_ASCON:
        plaintext = ascon.decrypt(ASCON_KEY, ASCON_NONCE, b"", ciphertext, variant="Ascon-128")
        return plaintext
    
    else:
        raise ValueError(f"Unsupported algorithm: {algo}")
