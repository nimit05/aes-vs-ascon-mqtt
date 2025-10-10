import paho.mqtt.client as mqtt
from config import BROKER, PORT, TOPIC
from aes_module import aes_decrypt
from ascon_module import ascon_decrypt
from metrics import measure_encryption

ALGO = "AES"  # Must match publisher

def on_message(client, userdata, msg):
    try:
        ciphertext, tag = msg.payload.split(b"||")

        if ALGO == "AES":
            plaintext, metrics = measure_encryption(aes_decrypt, ciphertext, tag)
        else:
            plaintext, metrics = measure_encryption(ascon_decrypt, ciphertext)

        print(f"Received (decrypted, {ALGO}): {plaintext}")  # plaintext is already str
        print("Decryption metrics:", metrics)
    except Exception as e:
        print("Decryption error:", e)

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)
print("Subscriber running...")
client.loop_forever()
