#include <Arduino.h>
#include <AX12.h>
#include <Servo.h>

#define LOW_POSITION 0
#define HIGH_POSITION 1
#define OTHER 2
#define MOVE_DOWN 3
#define MOVE_UP 4
#define FRONT 0
#define BACK 1

#define e1_pin_high 27
#define e1_pin_low  33
#define e2_pin_high 14
#define e2_pin_low  25
#define e3_pin_high 18 //a corriger
#define e3_pin_low  34 //a corriger
#define flag_pin_high 19 //a corriger
#define flag_pin_low 23 //a corriger

#define clamp0_pin  15
#define clamp1_pin  4
#define clamp2_pin  0
#define clamp3_pin  2
#define clamp4_pin  13
#define arm_pin  12

#define closed_clamp_state 0
#define open_clamp_state 1

#define open_clamp0_position 100
#define closed_clamp0_position 25
#define open_clamp1_position 100
#define closed_clamp1_position 15
#define open_clamp2_position 100
#define closed_clamp2_position 25
#define open_clamp3_position 100
#define closed_clamp3_position 25
#define open_clamp4_position 100
#define closed_clamp4_position 10

#define open_clamp_position 100
#define closed_clamp_position 20

#define folded_windsock_state 0
#define unfolded_windsock_state 1
#define end_windsock_state 2

#define folded_windsock_arm 180
#define unfolded_windsock_arm 100
#define end_windsock_arm 0


class Elevator
{
public:
    Elevator(uint8_t position, AX12 frontAX, AX12 backAX, uint8_t frontID, uint8_t backID);
    void begin(uint8_t id_front, uint8_t id_back);
    void setPosition(uint8_t position);
    int getPosition();
    void goTo(uint8_t height);
    void stop();
    void checkPosition(uint8_t pinHigh, uint8_t pinLow);
    void calibrate();

private:
    uint8_t _position;
    AX12 _frontAX;
    AX12 _backAX;
    uint8_t _frontID;
    uint8_t _backID;
};

class Clamp
{
public:
    Clamp(Servo servo, uint8_t state);
    void attach(uint8_t pin);
    void open();
    void close();
    void move(int position);

private:
    Servo _servo;
    uint8_t _state;
};

class WindsockArm
{
public:
    WindsockArm(Servo armServo, uint8_t armState);
    void attach(uint8_t pin);
    void unfold();
    void fold();
    void end();
    void moveArm(int position);

private:
    Servo _armServo;
    uint8_t _armState;
};

class Flag
{
public:
    Flag(uint8_t position, AX12 flagAX, uint8_t flagID);
    void begin(uint8_t id_AX);
    void setAXPosition(uint8_t position);
    int getAXPosition();
    void goTo(uint8_t height);
    void stop();
    void raiseFlag();
    void lowerFlag();
    void checkPosition(uint8_t pinHigh, uint8_t pinLow, WindsockArm *arm);
    void calibrate();

private:
    uint8_t _position;
    AX12 _flagAX;
    uint8_t _flagID;
};