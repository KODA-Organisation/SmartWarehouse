#ifndef ULTRASONIC_H
#define ULTRASONIC_H

class UltraSonic{
    public:
        int TRIGGER_PIN;
        int ECHO_PIN;

        UltraSonic(int TRIG_PIN, int ECHO_PIN);

        void Init();
        void SendTrigg();
        // long CatchEcho();
};

long GetDistance(UltraSonic& US);

#endif