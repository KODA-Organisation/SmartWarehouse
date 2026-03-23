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
        void Stop();
}; 

#endif