#include "instructions.h"

#include "../common/SerialTalks.h"

void ON(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    digitalWrite(13, HIGH);
}

void OFF(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    digitalWrite(13, LOW);
}