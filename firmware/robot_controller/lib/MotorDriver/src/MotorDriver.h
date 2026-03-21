#ifndef MOTORDRIVER_H
#define MOTORDRIVER_H

class Motor{
    public:
        int INF;
        int INS;

        // Declare constructor
        Motor(int first, int second);

        // Declare funcs
        void Init();
        void Move();
}; 

// INF - INPUT FIRST
// INS - INPUT SECOND
void MoveForward(Motor& M1, Motor& M2);

#endif