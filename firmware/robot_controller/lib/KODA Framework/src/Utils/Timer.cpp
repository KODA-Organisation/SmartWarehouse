#include<iostream>
#include<Utils/Timer.h>

Timer::Timer():seconds(0),shouldClose(false){}

long Timer::GetSeconds(){
    return seconds;
}   

float Timer::GetMinutes(){
    return seconds/60.0f;
}

float Timer::GetHours(){
    return seconds/3600.0f;
}

void Timer::Run(){
    while(!shouldClose){
        seconds++;
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
    // if something will cause end of cycle - task should terminate itself
    taskHandle = nullptr;
    vTaskDelete(NULL);
}

// This is C-like thingy
void Timer::Start(){
    // "Exception"
    if(taskHandle != nullptr) return;

    xTaskCreatePinnedToCore(
        TaskPoster, // what to do
        "Timer", // name
        2048,   // stack size
        this,   // object pointer
        1,      // Priority
        &taskHandle, // make freertos know how to access task
        1       // which core
    );
}

void Timer::Stop(){
    if(taskHandle != nullptr){
        shouldClose = true;
        // vTaskDelete(taskHandle);
        // taskHandle = NULL;
    }
}

void Timer::TaskPoster(void* config){
    // Get task from abstract 
    Timer* instance = static_cast<Timer*>(config);
    // Make it work, lmao
    instance-> Run();
}
