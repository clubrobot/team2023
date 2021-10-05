#include "topics.h"

#include "../common/SerialTalks.h"

static int i = 0;

void SUBSCRIPTION(Serializer &output)
{
    output.write<int>(i++);
}