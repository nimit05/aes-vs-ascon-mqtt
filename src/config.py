# config.py

# AES configuration
AES_KEY = b"ThisIsASecretKey!"   # 16 bytes (128-bit key)
AES_NONCE = b"fixednonce123"     # 12 bytes (must match between pub/sub)

# ASCON configuration
ASCON_KEY = b"thisisasconkey12"  # 16 bytes
ASCON_NONCE = b"fixedasconnonce" # 16 bytes

# MQTT broker settings
BROKER = "localhost"
PORT = 1883
TOPIC = "iot/messages"
