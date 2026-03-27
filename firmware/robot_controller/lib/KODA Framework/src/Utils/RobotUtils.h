#include <Motor/MotorDriver.h>
#include <UltraSonic/UltraSonic.h>

#ifndef ROBOTUTILS_H
#define ROBOTUTILS_H

class Robot{
    Motor LeftMotor;
    Motor RightMotor;
    UltraSonic US;
    public:
        Robot(Motor& L, Motor& R, UltraSonic& US);
        // Robot(int IN1, int IN2, int IN3, int IN4, int TRIGG_PIN, int ECHO_PIN);

        void Assemble();

        long CheckDistance();
        void MoveForward();
        // void Turn(float deg); // I want to do truning by degrees, but we need encoder (we dont have any)
        void TurnLeft();
        void TurnRight();
        void FullStop();
};

#endif