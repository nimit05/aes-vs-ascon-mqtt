extern "C" {
  #include "api.h"
  #include "ascon.h"

  int crypto_aead_encrypt(
    unsigned char *c,
    unsigned long long *clen,
    const unsigned char *m,
    unsigned long long mlen,
    const unsigned char *ad,
    unsigned long long adlen,
    const unsigned char *nsec,
    const unsigned char *npub,
    const unsigned char *k);

  int crypto_aead_decrypt(
    unsigned char *m,
    unsigned long long *mlen,
    unsigned char *nsec,
    const unsigned char *c,
    unsigned long long clen,
    const unsigned char *ad,
    unsigned long long adlen,
    const unsigned char *npub,
    const unsigned char *k);
}

// Key, nonce, and message
uint8_t key[16]   = {0};
uint8_t nonce[16] = {0};
uint8_t plaintext[] = "Hello! This is the test for ASCON  in esp8266";

// Buffers
uint8_t ciphertext[128];
uint8_t decrypted[128];

unsigned long long clen;
unsigned long long mlen;

unsigned long lastTime = 0;
const unsigned long interval = 5000; // 5 seconds
const int N = 50; // number of iterations per cycle for averaging

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("ESP8266 Ascon Benchmark Starting...");
}

void loop() {
  unsigned long now = millis();
  if (now - lastTime >= interval) {
    lastTime = now;

    Serial.println("\n--- New Benchmark Cycle ---");
    Serial.print("Free heap before: "); Serial.println(ESP.getFreeHeap());

    // --- Encryption Benchmark ---
    unsigned long totalEncryptTime = 0;
    for(int i = 0; i < N; i++) {
      unsigned long start = micros();
      crypto_aead_encrypt(ciphertext, &clen,
                          plaintext, sizeof(plaintext)-1,
                          NULL, 0, NULL, nonce, key);
      totalEncryptTime += micros() - start;
    }
    float avgEncrypt = totalEncryptTime / (float)N;
    float encryptKBps = (sizeof(plaintext)-1) / (avgEncrypt / 1e6) / 1024.0;

    Serial.print("Average encryption time (us): "); Serial.println(avgEncrypt);
    Serial.print("Encryption throughput (KB/s): "); Serial.println(encryptKBps);

    // Print one ciphertext sample
    Serial.print("Ciphertext (sample): ");
    for(unsigned long long i = 0; i < clen; i++)
      Serial.printf("%02X ", ciphertext[i]);
    Serial.println();

    // --- Decryption Benchmark ---
    unsigned long totalDecryptTime = 0;
    int ret = 0;
    for(int i = 0; i < N; i++) {
      unsigned long start = micros();
      ret = crypto_aead_decrypt(decrypted, &mlen,
                                NULL,
                                ciphertext, clen,
                                NULL, 0,
                                nonce, key);
      totalDecryptTime += micros() - start;
    }
    float avgDecrypt = totalDecryptTime / (float)N;
    float decryptKBps = (sizeof(plaintext)-1) / (avgDecrypt / 1e6) / 1024.0;

    Serial.print("Average decryption time (us): "); Serial.println(avgDecrypt);
    Serial.print("Decryption throughput (KB/s): "); Serial.println(decryptKBps);

    // Print decrypted plaintext
    if(ret == 0) {
      Serial.print("Decrypted plaintext: ");
      for(unsigned long long i = 0; i < mlen; i++)
        Serial.print((char)decrypted[i]);
      Serial.println();
    } else {
      Serial.println("Decryption failed!");
    }

    Serial.print("Free heap after: "); Serial.println(ESP.getFreeHeap());
    Serial.println("--- End of Benchmark Cycle ---\n");

    delay(100); // tiny delay to prevent loop flooding
  }
}
