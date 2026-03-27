#include <Arduino.h>
#include <Utils/RobotUtils.h>

// constexpr - must be init at compile time
// const - in compile or runtime

constexpr uint8_t TRIGGER_PIN = 42;
constexpr uint8_t ECHO_PIN = 41;
constexpr uint8_t IN1 = 4;
constexpr uint8_t IN2 = 5;
constexpr uint8_t IN3 = 6;
constexpr uint8_t IN4 = 7;

//Creating Motors
Motor Left(IN1, IN2);
Motor Right(IN3, IN4);

// Creating UltraSonic
UltraSonic US1(TRIGGER_PIN, ECHO_PIN);

// Creating a Robot object
Robot ROBOT(Left, Right, US1);
// Robot ROBOT(IN1, IN2, IN3, IN4, TRIGGER_PIN, ECHO_PIN);

bool moving = false;
bool obstacle = false;
void setup() {
    Serial.begin(115200);
    ROBOT.Assemble();
}

void loop() {
    // rm delay() 
    // make millis here
    long dist = ROBOT.CheckDistance();

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