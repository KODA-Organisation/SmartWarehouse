#include <Arduino.h>
#include <UltraSonic.h>
#include <MotorDriver.h>
#include <RobotUtils.h>

const int TRIGGER_PIN = 42;
const int ECHO_PIN = 41;
const int IN1 = 4;
const int IN2 = 5;
const int IN3 = 6;
const int IN4 = 7;

// Creating Motors
// Motor Left(IN1, IN2);
// Motor Right(IN3, IN4);

// // Creating UltraSonic
// UltraSonic US1(TRIGGER_PIN, ECHO_PIN);

// Creating a Robot object
Robot ROBOT(IN1, IN2, IN3, IN4, TRIGGER_PIN, ECHO_PIN);

// Robot ROBOT(Left, Right, US1);

bool moving = false;
bool obstacle = false;
void setup() {
    Serial.begin(115200);
    ROBOT.Assemble();
}

void loop() {
    long dist = GetDistance(ROBOT.US);

    if(dist < 30){
        obstacle = true;
    }else{
        obstacle = false;
    }

    if(!moving && !obstacle){
        ROBOT.MoveForward();
        moving = true;
    }else if(moving && obstacle){
        ROBOT.FullStop();
        moving = false;
    }

    Serial.println(dist);
    
    delay(600);
}