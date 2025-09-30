import paho.mqtt.client as mqtt
import time
from config import BROKER, PORT, TOPIC
from aes_module import aes_encrypt
from ascon_module import ascon_encrypt
from metrics import measure_encryption

ALGO = "AES"  # or "ASCON"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

for i in range(5):
    plaintext = f"Hello MQTT {i}".encode()

    # Measure encryption metrics
    if ALGO == "AES":
        (ciphertext, tag), metrics = measure_encryption(aes_encrypt, plaintext)
    else:
        (ciphertext, tag), metrics = measure_encryption(ascon_encrypt, plaintext)

    payload = ciphertext + b"||" + tag
    client.publish(TOPIC, payload)

    print(f"Sent (encrypted, {ALGO}): {payload}")
    print("Encryption metrics:", metrics)
    time.sleep(1)

client.disconnect()
