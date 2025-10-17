import paho.mqtt.client as mqtt
from config import BROKER, PORT, TOPIC
from crypto_manager import decrypt, ALGO_AES, ALGO_ASCON
from metrics import measure_encryption

ALGO = ALGO_AES  # Must match publisher

def on_message(client, userdata, msg):
    try:
        if ALGO == ALGO_AES:
            encrypted_b64, tag_b64 = msg.payload.split(b"||")
        else:
            encrypted_b64, tag_b64 = msg.payload, None

        (plaintext, metrics) = measure_encryption(decrypt, encrypted_b64, ALGO, tag_b64)

        if plaintext:
            print(f"\n[Subscriber] Received ({ALGO}): {plaintext.decode()}")
            print("[Subscriber Metrics]", metrics)
        else:
            print("[Subscriber] Decryption returned None!")

    except Exception as e:
        print("Decryption error:", e)
        print("------------------------------------------------------------")

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)
print("Subscriber running...")
client.loop_forever()
