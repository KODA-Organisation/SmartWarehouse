#include <MotorDriver.h>
#include <Arduino.h>

Motor::Motor(int first, int second){
    INF = first;
    INS = second;
}

void Motor::Init(){
    pinMode(INF, OUTPUT);
    pinMode(INS, OUTPUT);
}

// Main thing to make first - High, second - LOW
// To make it "circulate"
void Motor::Move(){
    digitalWrite(INF, HIGH);
    digitalWrite(INS, LOW);
}

// Move - makes HIGH to diff motor
void MoveForward(Motor& M1, Motor& M2){
    M1.Move();
    M2.Move();
}