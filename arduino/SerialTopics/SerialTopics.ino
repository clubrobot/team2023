#include <Arduino.h>

#include "instructions.h"
#include "topics.h"

#include "../common/SerialTalks.h"
#include "../common/SerialTopics.h"

void setup()
{
    // Communication
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
    topics.begin(talks);

    // bind functions
    talks.bind(ON_OPCODE, ON);
    talks.bind(OFF_OPCODE, OFF);

    //bind subscription
    topics.bind(SUBSCRIPTION_OPCODE, SUBSCRIPTION);

    pinMode(13, OUTPUT);
}

// Loop

void loop()
{
    talks.execute();
    topics.execute();
}
