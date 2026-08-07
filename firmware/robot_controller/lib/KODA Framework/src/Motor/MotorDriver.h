#ifndef MOTORDRIVER_H
#define MOTORDRIVER_H

class Motor{
    uint8_t INF;
    uint8_t INS;
    public:
        // Getters        
        uint8_t GetFirstPin();
        uint8_t GetSecondPin();

        // Declare constructor
        Motor(int first, int second);

        // Declare funcs
        void Init();
        void Move();
        void Stop();
}; 

#endif

// https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html