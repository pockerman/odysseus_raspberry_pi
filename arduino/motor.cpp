#include "motor.h"
#include <Arduino.h>
#include <math.h>

namespace motors
{

  Motor::Motor(const char* name, uint8_t in1, uint8_t in2,
          uint8_t enable, uint8_t max_speed)
  :
  name_(name),
  in1_pin_(in1),
  in2_pin_(in2),
  enable_pin_(enable),
  max_speed_(max_speed),
  current_speed_(0),
  is_stopped_(true)
  {
    //these are output from the Arduino and into
    //the L298N bridge
    pinMode(in1_pin_,OUTPUT);
    pinMode(in2_pin_,OUTPUT);
    pinMode(enable_pin_,OUTPUT);
  }

  void
  Motor::stop(){

    digitalWrite(in1_pin_,LOW);
    digitalWrite(in2_pin_,LOW);
    analogWrite(enable_pin_, 0);
    is_stopped_ = true;
  }

  void
  Motor::forward(const uint8_t speed){

    digitalWrite(in1_pin_, HIGH);
    digitalWrite(in2_pin_, LOW);

    //here speed specifies the duty cycle and should be
    //between [0,255] 0 = always off, 255 = always on
    current_speed_ = clamp_speed_to_max_(speed);
    analogWrite(enable_pin_,current_speed_);
    is_stopped_ = false;
  }

  void
  Motor::backward(const uint8_t speed){
    digitalWrite(in1_pin_,LOW);
    digitalWrite(in2_pin_,HIGH);

    current_speed_ = clamp_speed_to_max_(speed);
    analogWrite(enable_pin_,current_speed_);
    is_stopped_ = false;
  }

  uint8_t
  Motor::clamp_speed_to_max_(const uint8_t speed){

    if(speed > 255)
      return max_speed_;

    return speed;

  }

}


