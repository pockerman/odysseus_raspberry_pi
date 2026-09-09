#include <motor.h>

using namespace motors;

// Pin arrangement for the right motor
const uint8_t R_F_PIN = 0;
const uint8_t R_B_PIN = 1;
const uint8_t R_E_PIN = 3;

// Pin arrangement for the left motor
const uint8_t L_F_PIN = 0;
const uint8_t L_B_PIN = 1;
const uint8_t L_E_PIN = 3;

// The right motor
Motor r_motor("r_motor", R_F_PIN, R_B_PIN, R_E_PIN);

// The left motor
Motor l_motor("l_motor", L_F_PIN, L_B_PIN, L_E_PIN);

void setup() {
  
  // enable the two motors
  r_motor.enable();
  l_motor.enable();

}

void loop() {
  
  if (Serial.available()) {
    incomingMessage = Serial.readStringUntil('\n');
    incomingMessage.trim();  // Remove whitespace and newline

    if (incomingMessage == "ON") {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("LED is ON");
    } else if (incomingMessage == "OFF") {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("LED is OFF");
    } else {
      Serial.println("Unknown command");
    }
  }

}
