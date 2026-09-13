#ifndef ULTRASONIC_SENSOR_H
#define ULTRASONIC_SENSOR_H

#include <Arduino.h>

namespace odysseus
{

class HCSR04_UltrasonicSensor
{
public:
    HCSR04_UltrasonicSensor(uint8_t trig_pin, uint8_t echo_pin);

    float distance_cm();

private:
    uint8_t trig_pin_;
    uint8_t echo_pin_;

    static constexpr unsigned long DEFAULT_TIMEOUT_US = 30000;
};

}
#endif