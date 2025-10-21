import paho.mqtt.client as mqtt
from config import BROKER, PORT, TOPIC
from crypto_manager import encrypt, ALGO_AES, ALGO_ASCON
from metrics import measure_encryption

ALGO = ALGO_ASCON  # or ALGO_AES

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

messages = [
    b"Hello",  # 5 bytes (tiny)
    b"Secure IoT message",
    b"Temperature: 26.5C; Humidity: 45%; CO2: 400ppm",  # ~50 bytes
    b"A" * 256,   # 256 bytes    (small sensor packet)
    b"B" * 1024,  # 1 KB         (firmware meta)
    b"C" * 4096,  # 4 KB         (log data)
    b"D" * 16384  # 16 KB        (file/chunk upload)
]


for msg in messages:
    (result, metrics) = measure_encryption(encrypt, msg, ALGO)
    ciphertext, tag = result

    # Combine ciphertext + tag (if AES)
    if tag:
        payload = ciphertext + b"||" + tag
    else:
        payload = ciphertext

    client.publish(TOPIC, payload)
    # print(f"\n[Publisher] Sent ({ALGO}): {msg.decode()}")
    print("[Publisher Metrics]", metrics)

client.disconnect()
