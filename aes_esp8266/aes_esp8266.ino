#include <Arduino.h>
extern "C" {
    #include "aes.h"
}

// =================== AES-192 CBC Setup ===================
uint8_t aesKey[24] = {
    0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,
    0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,
    0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17
};

uint8_t iv[16] = {
    0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,
    0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F
};

const char* plaintext = "This is a test message for AES-192 CBC on ESP8266!";
uint32_t interval = 5000; // 5 seconds
uint32_t lastTime = 0;

AES_ctx ctx;

void printHex(uint8_t* data, size_t len){
    for(size_t i=0;i<len;i++){
        if(data[i]<16) Serial.print("0");
        Serial.print(data[i],HEX); Serial.print(" ");
    }
    Serial.println();
}

void setup(){
    Serial.begin(115200);
    Serial.println("=== AES-192 CBC Benchmark ===");
}

void loop(){
    if(millis()-lastTime>=interval){
        lastTime = millis();

        size_t len = strlen(plaintext);
        size_t paddedLen = ((len+15)/16)*16;
        uint8_t buffer[paddedLen];
        memset(buffer,0,paddedLen);
        memcpy(buffer,plaintext,len);

        uint8_t encrypted[paddedLen];
        uint8_t decrypted[paddedLen];

        // Number of iterations for averaging
        const int N = 10;
        uint32_t totalEnc = 0, totalDec = 0;

        for(int i=0;i<N;i++){
            memcpy(encrypted, buffer, paddedLen);
            memcpy(ctx.Iv, iv, 16); // reset IV
            AES_init_ctx_iv(&ctx, aesKey, iv);

            uint32_t startEnc = micros();
            AES_CBC_encrypt_buffer(&ctx, encrypted, paddedLen);
            uint32_t endEnc = micros();
            totalEnc += (endEnc-startEnc);

            memcpy(decrypted, encrypted, paddedLen);
            memcpy(ctx.Iv, iv, 16); // reset IV
            AES_init_ctx_iv(&ctx, aesKey, iv);

            uint32_t startDec = micros();
            AES_CBC_decrypt_buffer(&ctx, decrypted, paddedLen);
            uint32_t endDec = micros();
            totalDec += (endDec-startDec);
        }

        Serial.println("--- AES-192 CBC Cycle ---");
        Serial.print("Plaintext: "); Serial.println(plaintext);

        Serial.print("Ciphertext: "); printHex(encrypted,paddedLen);

        Serial.print("Decrypted: ");
        for(size_t i=0;i<len;i++) Serial.print((char)decrypted[i]);
        Serial.println();

        // Average time in microseconds
        uint32_t avgEnc = totalEnc/N;
        uint32_t avgDec = totalDec/N;

        Serial.print("Average Encryption time (µs): "); Serial.println(avgEnc);
        Serial.print("Average Decryption time (µs): "); Serial.println(avgDec);

        float encThroughput = (float)paddedLen / avgEnc * 1000000 / 1024.0; // KB/s
        float decThroughput = (float)paddedLen / avgDec * 1000000 / 1024.0; // KB/s

        Serial.print("Encryption Throughput (KB/s): "); Serial.println(encThroughput,2);
        Serial.print("Decryption Throughput (KB/s): "); Serial.println(decThroughput,2);

        Serial.print("Free Heap: "); Serial.println(ESP.getFreeHeap());
        Serial.println("--- End of Cycle ---\n");
    }
}
