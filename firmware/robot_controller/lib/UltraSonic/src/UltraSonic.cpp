#include <UltraSonic.h>
#include <Arduino.h>

constexpr float SOUND_SPEED_CM = 0.0343f;

long microsecondsToCentimeters(long microseconds);

long GetDistance(int TRIGGER_PIN, int ECHO_PIN){
    long duration, cm;
    // Trigg pulse
    digitalWrite(TRIGGER_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIGGER_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER_PIN, LOW);

    // Get echo
    // 3 arg - timeout
    duration = pulseIn(ECHO_PIN, HIGH, 30000);

    // debounce
    if (duration == 0) {
        return -1; 
    }

    return microsecondsToCentimeters(duration);
}

long microsecondsToCentimeters(long microseconds){
    return microseconds / 29 / 2;
}