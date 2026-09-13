#include <motor.h>
#include <hc_sr04_sensor.h>

using namespace odysseus;

// Pin arrangement for the right motor
const uint8_t R_F_PIN = 0;
const uint8_t R_B_PIN = 1;
const uint8_t R_E_PIN = 3;

// Pin arrangement for the left motor
const uint8_t L_F_PIN = 0;
const uint8_t L_B_PIN = 1;
const uint8_t L_E_PIN = 3;

// Pin arrangement for the front ultrasonic sensor
const uint8_t FRONT_TRIG_PIN = 4;
const uint8_t FRONT_ECHO_PIN = 5;

// Pin arrangement for the rear ultrasonic sensor
const uint8_t REAR_TRIG_PIN = 6;
const uint8_t REAR_ECHO_PIN = 7;

// The right motor
Motor r_motor("r_motor", R_F_PIN, R_B_PIN, R_E_PIN);

// The left motor
Motor l_motor("l_motor", L_F_PIN, L_B_PIN, L_E_PIN);

// The front and rear ultrasonic sensors
HCSR04_UltrasonicSensor front_sensor(FRONT_TRIG_PIN, FRONT_ECHO_PIN);
HCSR04_UltrasonicSensor rear_sensor(REAR_TRIG_PIN, REAR_ECHO_PIN);

String incomingMessage;

// Drive a single motor from a signed speed in [-255, 255]:
// positive is forward, negative is backward, zero stops it.
void apply_motor_command(Motor& motor, int speed) {
  if (speed > 0) {
    motor.forward((uint8_t)min(speed, 255));
  } else if (speed < 0) {
    motor.backward((uint8_t)min(-speed, 255));
  } else {
    motor.stop();
  }
}

// Reports the current PWM duty cycle of both motors together with the
// latest front/rear distance readings, e.g. "STATUS 80 60 23.40 100.10"
void send_status() {
  Serial.print("STATUS ");
  Serial.print(l_motor.get_current_speed());
  Serial.print(' ');
  Serial.print(r_motor.get_current_speed());
  Serial.print(' ');
  Serial.print(front_sensor.distance_cm());
  Serial.print(' ');
  Serial.println(rear_sensor.distance_cm());
}

void setup() {
  Serial.begin(115200);
}

void loop() {

  if (Serial.available()) {
    incomingMessage = Serial.readStringUntil('\n');
    incomingMessage.trim();  // Remove whitespace and newline

    // Commands are of the form "<type> <l>,<r>", e.g. "set 80,60" or "stop 0,0".
    // "status" takes no payload and only queries the sensors/motors as-is.
    int space_idx = incomingMessage.indexOf(' ');
    String cmd = space_idx == -1 ? incomingMessage : incomingMessage.substring(0, space_idx);

    if (cmd != "status") {
      int comma_idx = incomingMessage.indexOf(',');

      int l_speed = 0;
      int r_speed = 0;

      if (space_idx != -1 && comma_idx != -1) {
        l_speed = incomingMessage.substring(space_idx + 1, comma_idx).toInt();
        r_speed = incomingMessage.substring(comma_idx + 1).toInt();
      }

      apply_motor_command(l_motor, l_speed);
      apply_motor_command(r_motor, r_speed);
    }

    send_status();
  }
}
