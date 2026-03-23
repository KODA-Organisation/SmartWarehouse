#include <RobotUtils.h>

// IDK if this is needed, bc it is just wasting resources
// Robot::Robot(Motor& LMotor, Motor& RMotor, UltraSonic& US):
//     LeftMotor(LMotor.INF, LMotor.INS),
//     RightMotor(RMotor.INF, RMotor.INS),
//     US(US.TRIGGER_PIN, US.ECHO_PIN)
//     {}

// However this is less "comfy"
Robot::Robot(int IN1, int IN2, int IN3, int IN4, int TRIGG_PIN, int ECHO_PIN):
    LeftMotor(IN1, IN2),
    RightMotor(IN3, IN4),
    US(TRIGG_PIN, ECHO_PIN)
    {}

void Robot::Assemble(){
    LeftMotor.Init();
    RightMotor.Init();
    US.Init();
}

// Move - makes HIGH to diff motor
void Robot::MoveForward(){
    LeftMotor.Move();
    RightMotor.Move();
}

void Robot::FullStop(){
    LeftMotor.Stop();
    RightMotor.Stop();
}