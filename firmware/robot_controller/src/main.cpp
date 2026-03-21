#include <Arduino.h>
#include <UltraSonic.h>
#include <MotorDriver.h>

const int TRIGGER_PIN = 42;
const int ECHO_PIN = 41;
const int IN1 = 4;
const int IN2 = 5;
const int IN3 = 6;
const int IN4 = 7;

// Creating Motors
Motor Left(4,5);
Motor Right(6,7);

bool moving = false;

void setup() {
    Serial.begin(115200);
    pinMode(TRIGGER_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    Left.Init();
    Right.Init();
}

void loop() {
    if(!moving){
        MoveForward(Left, Right);
        moving = true;
    }
    Serial.println(GetDistance(TRIGGER_PIN, ECHO_PIN));
    delay(60);
}