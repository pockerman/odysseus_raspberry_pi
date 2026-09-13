#include <motor.h>
#include <hc_sr04_sensor.h>

using namespace odysseus;

// ============================================================
// PIN CONFIGURATION
// ============================================================

// Left motor
constexpr uint8_t LEFT_IN1 = 6;
constexpr uint8_t LEFT_IN2 = 7;
constexpr uint8_t LEFT_EN = 5;

// Right motor
constexpr uint8_t RIGHT_IN1 = 9;
constexpr uint8_t RIGHT_IN2 = 10;
constexpr uint8_t RIGHT_EN = 3;

// Front ultrasonic
constexpr uint8_t FRONT_TRIG = 11;
constexpr uint8_t FRONT_ECHO = 12;

// Rear ultrasonic
constexpr uint8_t REAR_TRIG = 13;
constexpr uint8_t REAR_ECHO = A0;

Motor left_motor(
    "left",
    LEFT_IN1,
    LEFT_IN2,
    LEFT_EN
);

Motor right_motor(
    "right",
    RIGHT_IN1,
    RIGHT_IN2,
    RIGHT_EN
);

HCSR04_UltrasonicSensor front_sensor(
    FRONT_TRIG,
    FRONT_ECHO
);

HCSR04_UltrasonicSensor rear_sensor(
    REAR_TRIG,
    REAR_ECHO
);

constexpr unsigned long SERIAL_BAUD = 115200;

// If Raspberry Pi doesn't send a command within this
// amount of time, stop both motors.
constexpr unsigned long COMMAND_TIMEOUT_MS = 1000;

// Send STATUS every 200 ms.
constexpr unsigned long STATUS_INTERVAL_MS = 200;

// ============================================================
// STATE
// ============================================================

int left_command = 0;
int right_command = 0;

unsigned long last_command_time = 0;
unsigned long last_status_time = 0;

// ============================================================
// MOTOR CONTROL
// ============================================================

void setMotor(Motor& motor, int speed)
{
    // Forward
    if (speed > 0)
    {
        motor.forward(
            static_cast<uint8_t>(speed)
        );
    }

    // Backward
    else if (speed < 0)
    {
        motor.backward(
            static_cast<uint8_t>(-speed)
        );
    }

    // Stop
    else
    {
        motor.stop();
    }
}


void setMotors(int left, int right)
{
    // Limit commands to [-255, 255]

    left = constrain(left, -255, 255);
    right = constrain(right, -255, 255);

    left_command = left;
    right_command = right;

    setMotor(left_motor, left);
    setMotor(right_motor, right);
}


// ============================================================
// STOP
// ============================================================

void stopMotors()
{
    left_command = 0;
    right_command = 0;

    left_motor.stop();
    right_motor.stop();
}

// ============================================================
// SERIAL COMMAND HANDLING
// ============================================================

void processCommand(String command)
{
    command.trim();

    if (command.length() == 0)
        return;


    // --------------------------------------------------------
    // STOP
    // --------------------------------------------------------

    if (command == "STOP")
    {
        stopMotors();

        last_command_time = millis();

        Serial.println("OK STOP");

        return;
    }


    // --------------------------------------------------------
    // SET <left> <right>
    //
    // Example:
    //
    // SET 120 100
    //
    // Positive = forward
    // Negative = backward
    // 0 = stop
    // --------------------------------------------------------

    if (command.startsWith("SET "))
    {
        int left;
        int right;

        int result = sscanf(
            command.c_str(),
            "SET %d %d",
            &left,
            &right
        );

        if (result == 2)
        {
            left = constrain(left, -255, 255);
            right = constrain(right, -255, 255);

            setMotors(left, right);

            last_command_time = millis();

            Serial.print("OK ");
            Serial.print(left_command);
            Serial.print(" ");
            Serial.println(right_command);

            return;
        }
    }


    // --------------------------------------------------------
    // Unknown command
    // --------------------------------------------------------

    Serial.print("ERROR UNKNOWN_COMMAND ");
    Serial.println(command);
}

// ============================================================
// SERIAL INPUT
// ============================================================

void readSerial()
{
    static String input;

    while (Serial.available() > 0)
    {
        char c = Serial.read();

        if (c == '\n')
        {
            processCommand(input);

            input = "";
        }
        else if (c != '\r')
        {
            input += c;
        }
    }
}

// ============================================================
// STATUS
// ============================================================

void sendStatus()
{
    float front_distance = front_sensor.distanceCm();

    // Small delay between ultrasonic measurements.
    // This helps prevent acoustic interference.
    delay(5);

    float rear_distance = rear_sensor.distanceCm();


    Serial.print("STATUS ");

    // Motor commands
    Serial.print(left_command);
    Serial.print(" ");

    Serial.print(right_command);
    Serial.print(" ");


    // RPM placeholders
    //
    // These will be replaced when we add
    // wheel encoders.
    Serial.print(0);
    Serial.print(" ");

    Serial.print(0);
    Serial.print(" ");


    // Distances
    Serial.print(front_distance, 1);
    Serial.print(" ");

    Serial.println(rear_distance, 1);
}


// ============================================================
// WATCHDOG
// ============================================================

void checkWatchdog()
{
    unsigned long now = millis();

    if (now - last_command_time > COMMAND_TIMEOUT_MS)
    {
        if (!left_motor.isStopped() ||
            !right_motor.isStopped())
        {
            stopMotors();

            Serial.println("WATCHDOG STOP");
        }
    }
}

// ============================================================
// SETUP
// ============================================================

void setup()
{
    Serial.begin(SERIAL_BAUD);

    // Initial safe state
    stopMotors();

    last_command_time = millis();
    last_status_time = millis();

    Serial.println("READY");
}

// ============================================================
// LOOP
// ============================================================

void loop()
{
    unsigned long now = millis();


    // --------------------------------------------------------
    // 1. Read commands from Raspberry Pi
    // --------------------------------------------------------

    readSerial();


    // --------------------------------------------------------
    // 2. Safety watchdog
    // --------------------------------------------------------

    checkWatchdog();


    // --------------------------------------------------------
    // 3. Periodic status
    // --------------------------------------------------------

    if (now - last_status_time >= STATUS_INTERVAL_MS)
    {
        last_status_time = now;

        sendStatus();
    }
}