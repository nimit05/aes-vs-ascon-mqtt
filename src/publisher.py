import paho.mqtt.client as mqtt
from config import BROKER, PORT, TOPIC
from crypto_manager import encrypt, ALGO_AES, ALGO_ASCON
from metrics import measure_encryption

ALGO = ALGO_AES  # or ALGO_AES

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

messages = [b"Hello", b"Secure IoT", b"Final Test"]

for msg in messages:
    (result, metrics) = measure_encryption(encrypt, msg, ALGO)
    ciphertext, tag = result

    # Combine ciphertext + tag (if AES)
    if tag:
        payload = ciphertext + b"||" + tag
    else:
        payload = ciphertext

    client.publish(TOPIC, payload)
    print(f"\n[Publisher] Sent ({ALGO}): {msg.decode()}")
    print("[Publisher Metrics]", metrics)

client.disconnect()
