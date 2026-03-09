#include <Arduino.h>

const int trigPin = 8;
const int echoPin = 9;

void setup() {
    Serial.begin(115200);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    Serial.println("Радар активирован. Ищем препятствия...");
}

void loop() {
    // Очищаем пин перед выстрелом
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    // Стреляем ультразвуком (импульс 10 микросекунд)
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    // Засекаем, через сколько микросекунд вернулось эхо
    long duration = pulseIn(echoPin, HIGH);

    // Формула перевода времени в сантиметры (скорость звука)
    int distance = duration * 0.034 / 2;

    Serial.print("Дистанция: ");
    Serial.print(distance);
    Serial.println(" см");

    delay(500);
}