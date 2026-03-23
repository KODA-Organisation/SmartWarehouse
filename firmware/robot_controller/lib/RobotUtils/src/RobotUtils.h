#include <MotorDriver.h>
#include <UltraSonic.h>

#ifndef ROBOTUTILS_H
#define ROBOTUTILS_H

class Robot{
    public:
        Motor LeftMotor;
        Motor RightMotor;
        UltraSonic US;
        
        // Robot(Motor& L, Motor& R, UltraSonic& US);

        Robot(int IN1, int IN2, int IN3, int IN4, int TRIGG_PIN, int ECHO_PIN);

        void Assemble();

        void MoveForward();
        void FullStop();
};

#endif