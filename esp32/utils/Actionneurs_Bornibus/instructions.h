#ifndef __INSTRUCTIONS_H__
#define __INSTRUCTIONS_H__

#include <SerialTalks.h>

#define ERROR 3

#define MOVE_ELEVATOR_OPCODE 0X10
#define GET_ELEVATOR_POSITION_OPCODE 0X11
#define MOVE_CLAMP_OPCODE 0x12
#define SET_CLAMP_POSITION_OPCODE 0x13
#define MOVE_WINDSOCK_ARM_OPCODE 0x14
#define SET_WINDSOCK_ARM_POSITION_OPCODE 0x15
#define MOVE_FLAG_OPCODE 0x16
#define RAISE_FLAG_OPCODE 0x17
#define LOWER_FLAG_OPCODE 0x18
#define GET_FLAG_POSITION_OPCODE 0x19
#define CALIBRATE_ELEVATOR_OPCODE 0x20
#define CALIBRATE_FLAG_OPCODE 0x21

void MOVE_ELEVATOR(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_ELEVATOR_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output);
void MOVE_CLAMP(SerialTalks &inst, Deserializer &input, Serializer &output);
void SET_CLAMP_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output);
void MOVE_WINDSOCK_ARM(SerialTalks &inst, Deserializer &input, Serializer &output);
void SET_WINDSOCK_ARM_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output);
void MOVE_FLAG(SerialTalks &inst, Deserializer &input, Serializer &output);
void RAISE_FLAG(SerialTalks &inst, Deserializer &input, Serializer &output);
void LOWER_FLAG(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_FLAG_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output);
void CALIBRATE_ELEVATOR(SerialTalks &inst, Deserializer &input, Serializer &output);
void CALIBRATE_FLAG(SerialTalks &inst, Deserializer &input, Serializer &output);

#endif // __INSTRUCTIONS_H__
