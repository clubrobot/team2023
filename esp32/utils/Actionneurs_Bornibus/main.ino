#include <Arduino.h>
#include <AX12.h>
#include "BornibusActions.h"
#include <SerialTalks.h>
#include "instructions.h"
#include <Servo.h>

AX12 ax0;
AX12 ax1;
AX12 ax2;
AX12 ax3;
AX12 ax4;
AX12 ax5;
AX12 axFlag;

Servo s0;
Servo s1;
Servo s2;
Servo s3;
Servo s4;
Servo s5;

Elevator e1(OTHER, ax0, ax1, 6, 0);
Elevator e2(OTHER, ax2, ax3, 4, 1);
Elevator e3(OTHER, ax4, ax5, 7, 20);

Clamp clamp0(s0, closed_clamp_state);
Clamp clamp1(s1, closed_clamp_state);
Clamp clamp2(s2, closed_clamp_state);
Clamp clamp3(s3, closed_clamp_state);
Clamp clamp4(s4, closed_clamp_state);

WindsockArm arm(s5, folded_windsock_arm);
Flag sailFlag(OTHER, axFlag, 3);

void setup() {
  //Starting SerialTalks
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
    talks.bind(MOVE_ELEVATOR_OPCODE, MOVE_ELEVATOR);
    talks.bind(GET_ELEVATOR_POSITION_OPCODE, GET_ELEVATOR_POSITION);
    talks.bind(MOVE_CLAMP_OPCODE, MOVE_CLAMP);
    talks.bind(SET_CLAMP_POSITION_OPCODE, SET_CLAMP_POSITION);
    talks.bind(MOVE_WINDSOCK_ARM_OPCODE, MOVE_WINDSOCK_ARM);
    talks.bind(SET_WINDSOCK_ARM_POSITION_OPCODE, SET_WINDSOCK_ARM_POSITION);
    talks.bind(MOVE_FLAG_OPCODE, MOVE_FLAG);
    talks.bind(RAISE_FLAG_OPCODE, RAISE_FLAG);
    talks.bind(LOWER_FLAG_OPCODE, LOWER_FLAG);
    talks.bind(GET_FLAG_POSITION_OPCODE, GET_FLAG_POSITION);
    talks.bind(CALIBRATE_ELEVATOR_OPCODE, CALIBRATE_ELEVATOR);
    talks.bind(CALIBRATE_FLAG_OPCODE, CALIBRATE_FLAG);

    pinMode(e1_pin_high, INPUT_PULLUP);
    pinMode(e1_pin_low, INPUT_PULLUP);
    pinMode(e2_pin_high, INPUT_PULLUP);
    pinMode(e2_pin_low, INPUT_PULLUP);
    pinMode(e3_pin_high, INPUT_PULLUP);
    pinMode(e3_pin_low, INPUT_PULLUP);
    pinMode(flag_pin_high, INPUT_PULLUP);
    pinMode(flag_pin_low, INPUT_PULLUP);

  /*  pinMode(32, INPUT);
    pinMode(14, INPUT);
    pinMode(27, INPUT);
    pinMode(33, INPUT);
    pinMode(25, INPUT);
    pinMode(26, INPUT);*/

    AX12::SerialBegin(1000000, 5);
    e1.begin(6,0);
    e2.begin(4,1);
    e3.begin(7,20);

    clamp0.attach(clamp0_pin);
    clamp1.attach(clamp1_pin);
    clamp2.attach(clamp2_pin);
    clamp3.attach(clamp3_pin);
    clamp4.attach(clamp4_pin);

    arm.attach(arm_pin);
    sailFlag.begin(3);
}

void loop() {
  talks.execute();
  e1.checkPosition(e1_pin_high, e1_pin_low);
  e2.checkPosition(e2_pin_high, e2_pin_low);
  e3.checkPosition(e3_pin_high, e3_pin_low);
  sailFlag.checkPosition(flag_pin_high, flag_pin_low, &arm);
}
