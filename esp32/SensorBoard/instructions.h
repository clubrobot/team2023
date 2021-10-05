#ifndef __INSTRUCTIONS_H__
#define __INSTRUCTIONS_H__

#include <SerialTalks.h>

#define GET_SENSOR1_OPCODE 0x10
#define GET_SENSOR2_OPCODE 0x11
#define GET_SENSOR3_OPCODE 0x12
#define GET_SENSOR4_OPCODE 0x13
#define GET_SENSOR5_OPCODE 0x14
#define GET_SENSOR6_OPCODE 0x15
#define GET_SENSOR7_OPCODE 0x16
#define GET_SENSOR8_OPCODE 0x17

#define CHECK_ERROR_OPCODE 0x18

void GET_SENSOR1(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_SENSOR2(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_SENSOR3(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_SENSOR4(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_SENSOR5(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_SENSOR6(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_SENSOR7(SerialTalks &inst, Deserializer &input, Serializer &output);
void GET_SENSOR8(SerialTalks &inst, Deserializer &input, Serializer &output);

void CHECK_ERROR(SerialTalks &inst, Deserializer &input, Serializer &output);

#endif // __INSTRUCTIONS_H__
