#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

#ifndef TIMER_H
#define TIMER_H

class Timer{
    volatile long seconds;     // do not optimize this
    volatile bool shouldClose; // do not optimize this

    TaskHandle_t taskHandle = nullptr; // reference

    // idk how to explain this rn
    static void TaskPoster(void* config);

    // Definition what to do (in class)
    void Run();
    public:
        Timer();

        long GetSeconds();
        float GetMinutes();
        float GetHours();
        void Start();
        void Stop();
        void Pause();
        void Resume();
};

#endif