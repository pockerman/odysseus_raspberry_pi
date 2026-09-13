#include "hc_sr04_sensor.h"


namespace odysseus{

HCSR04_UltrasonicSensor::HCSR04_UltrasonicSensor(uint8_t trig_pin, uint8_t echo_pin)
    :
    trig_pin_(trig_pin),
    echo_pin_(echo_pin)
{
    pinMode(trig_pin_, OUTPUT);
    pinMode(echo_pin_, INPUT);

    digitalWrite(trig_pin_, LOW);
}

float HCSR04_UltrasonicSensor::distance_cm()
{
    // Make sure the trigger starts LOW
    digitalWrite(trig_pin_, LOW);
    delayMicroseconds(2);

    // Send a 10 us trigger pulse
    digitalWrite(trig_pin_, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig_pin_, LOW);

    // Measure the echo pulse
    unsigned long duration =
        pulseIn(echo_pin_, HIGH, DEFAULT_TIMEOUT_US);

    // No echo received
    if (duration == 0)
        return -1.0f;

    // Speed of sound ≈ 0.0343 cm/us.
    // Divide by 2 because the sound travels to the object and back.
    return (duration * 0.0343f) / 2.0f;
}
}