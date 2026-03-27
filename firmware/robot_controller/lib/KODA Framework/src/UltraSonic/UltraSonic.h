#ifndef ULTRASONIC_H
#define ULTRASONIC_H

class UltraSonic{
    uint8_t TRIGGER_PIN;
    uint8_t ECHO_PIN;
    public:
        // Getters
        uint8_t GetTriggerPin();
        uint8_t GetEchoPin();

        // Constructor
        UltraSonic(uint8_t TRIG_PIN, uint8_t ECHO_PIN);

        void Init();
        void SendTrigg();
        // long CatchEcho();
        long GetDistance();
};

#endif