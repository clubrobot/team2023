#include "instructions.h"

#include <SerialTalks.h>

void ON(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    digitalWrite(2, HIGH);
}

void OFF(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    digitalWrite(2, LOW);
}