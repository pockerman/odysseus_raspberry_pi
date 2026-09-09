#ifndef MOTOR_H
#define MOTOR_H

// use all the standard definitions of the Arduino language
#include "Arduino.h"

namespace motors
{
  // class Motor models an electric motor
  // controlled via an L298N bridge.
  class Motor
  {

  public:

    // The default max speed the motor can reach
    static uint8_t default_max_speed(){return 255;}

    // Constructor: Create a motor by passing the forward and backward pins as well
    // as the enable pin. Note that the enable pin must be PWM capable. Finally
    //  there is also an option to set the maximum speed of the motor
    Motor(const char* name, uint8_t in1, uint8_t in2,
          uint8_t enable, uint8_t max_speed=Motor::default_max_speed());

    // Stops the motor
    void stop();

    // Move the motor in the forward direction. This function simply sets the f_pin_ to HIGH and the b_pin_ to LOW
    void forward(const uint8_t speed);

    /// Move the motor in the reverse direction. This function simply sets the f_pin_ to LOW and the b_pin_ to HIGH
    void backward(const uint8_t speed);

    // Returns the id of the forward pin
    uint8_t get_in1_pin()const{return in1_pin_;}

    // Returns the id of the backward pin
    uint8_t get_in2_pin()const{return in2_pin_;}

    uint8_t get_max_speed()const{return max_speed_;}
    bool is_stopped()const{return is_stopped_;}
    uint8_t get_current_speed()const{return current_speed_;};

  private:

    const char* name_;

    // The forward pin
    uint8_t in1_pin_;

    // The backward pin that is the pin for moving the motor
    // in the reverse direction than f_pin_
    uint8_t in2_pin_;

    // The enable pin. It must be PWM capable
    uint8_t enable_pin_;

    // The max speed  the motor is capable of
    uint8_t max_speed_;

    uint8_t current_speed_;

    //flag indicating if the motor is stopped
    bool is_stopped_;

    uint8_t clamp_speed_to_max_(const uint8_t speed);
  };

}//motors

#endif

