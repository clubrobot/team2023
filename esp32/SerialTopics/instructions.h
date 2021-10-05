#ifndef __INSTRUCTIONS_H__
#define __INSTRUCTIONS_H__

#include <SerialTalks.h>

#define ON_OPCODE 0X10
#define OFF_OPCODE 0X11

void ON(SerialTalks &inst, Deserializer &input, Serializer &output);

void OFF(SerialTalks &inst, Deserializer &input, Serializer &output);

#endif // __INSTRUCTIONS_H__
