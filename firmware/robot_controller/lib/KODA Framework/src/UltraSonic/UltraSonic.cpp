#include <UltraSonic/UltraSonic.h>
#include <Arduino.h>

constexpr float SOUND_SPEED_CM = 0.0343f;

UltraSonic::UltraSonic(uint8_t TR_PIN, uint8_t ECH_PIN){
    TRIGGER_PIN = TR_PIN;
    ECHO_PIN = ECH_PIN;
}

uint8_t UltraSonic::GetTriggerPin(){
    return TRIGGER_PIN;
}
uint8_t UltraSonic::GetEchoPin(){
    return ECHO_PIN;
}

void UltraSonic::Init(){
    pinMode(TRIGGER_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
}

void UltraSonic::SendTrigg(){
    // Trigg pulse
    digitalWrite(TRIGGER_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIGGER_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER_PIN, LOW);
}

long microsecondsToCentimeters(long microseconds){
    return microseconds / 29 / 2;
}

long UltraSonic::GetDistance(){    
    // Triggering
    SendTrigg();
    long duration = pulseIn(ECHO_PIN, HIGH);
    // output
    return microsecondsToCentimeters(duration);
}