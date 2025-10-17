# config.py

# AES configuration
AES_KEY = b"ThisIsASecretKey"   # 16 bytes (128-bit key)
AES_NONCE = b"fixednonce123"     # 12 bytes (must match between pub/sub)

# ASCON configuration
ASCON_KEY = b"0123456789ABCDEF"      # 16 bytes = 128-bit key
ASCON_NONCE = b"1234567890ABCDEF"

# MQTT broker settings
BROKER = "localhost"
PORT = 1883
TOPIC = "iot/messages"
