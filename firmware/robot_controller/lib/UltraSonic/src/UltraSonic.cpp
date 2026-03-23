#include <UltraSonic.h>
#include <Arduino.h>

constexpr float SOUND_SPEED_CM = 0.0343f;

UltraSonic::UltraSonic(int TR_PIN, int ECH_PIN){
    TRIGGER_PIN = TR_PIN;
    ECHO_PIN = ECH_PIN;
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

long GetDistance(UltraSonic& US){    
    // Triggering
    US.SendTrigg();
    long duration = pulseIn(US.ECHO_PIN, HIGH);
    // output
    return microsecondsToCentimeters(duration);
}