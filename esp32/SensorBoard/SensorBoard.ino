#include <Arduino.h>
#include <list>

#include "instructions.h"
#include "topics.h"
#include "PIN.h"
#include "constants.h"

#include <Wire.h>
#include <SerialTalks.h>
#include <SerialTopics.h>
#include <ShiftRegister.h>
#include <VL53L0X.h>
#include <VL6180X.h>
#include <TaskManager.h>

using namespace std;

TaskManager tm;

ShiftRegister ShutdownRegister(SHIFT_REGISTER_2_BYTES);

VL53L0X vl53_1 = VL53L0X(VL53L0X_1_I2C_ADDR, VL53L0X_1_SHUTDOWN_INDEX, &ShutdownRegister);
VL53L0X vl53_2 = VL53L0X(VL53L0X_2_I2C_ADDR, VL53L0X_2_SHUTDOWN_INDEX, &ShutdownRegister);
VL53L0X vl53_3 = VL53L0X(VL53L0X_3_I2C_ADDR, VL53L0X_3_SHUTDOWN_INDEX, &ShutdownRegister);
VL53L0X vl53_4 = VL53L0X(VL53L0X_5_I2C_ADDR, VL53L0X_4_SHUTDOWN_INDEX, &ShutdownRegister);
VL53L0X vl53_5 = VL53L0X(VL53L0X_5_I2C_ADDR, VL53L0X_5_SHUTDOWN_INDEX, &ShutdownRegister);
VL53L0X vl53_6 = VL53L0X(VL53L0X_6_I2C_ADDR, VL53L0X_6_SHUTDOWN_INDEX, &ShutdownRegister);
VL53L0X vl53_7 = VL53L0X(VL53L0X_7_I2C_ADDR, VL53L0X_7_SHUTDOWN_INDEX, &ShutdownRegister);
VL53L0X vl53_8 = VL53L0X(VL53L0X_8_I2C_ADDR, VL53L0X_8_SHUTDOWN_INDEX, &ShutdownRegister);

list<VL53L0X *> sensors_vl53 = {&vl53_1, &vl53_2, &vl53_3, &vl53_4};

uint8_t vl53_status[VL53L0X_COUNT] = {0};

uint16_t vl53_measurement[VL53L0X_COUNT] = {10};

// serialtalks wrapper
void talksExecuteWrapper()
{
    talks.execute();
    topics.execute();
}

void setup()
{
    static int count = 0;

    // Attach shift register pin
    ShutdownRegister.attach(SHIFT_REG_LATCH, SHIFT_REG_CLOCK, SHIFT_REG_DATA);

    // I2C Communication
    Wire.begin();

    // Serial Communication
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
    topics.begin(talks);

    // bind functions
    talks.bind(GET_SENSOR1_OPCODE, GET_SENSOR1);
    talks.bind(GET_SENSOR2_OPCODE, GET_SENSOR2);
    talks.bind(GET_SENSOR3_OPCODE, GET_SENSOR3);
    talks.bind(GET_SENSOR4_OPCODE, GET_SENSOR4);
    talks.bind(GET_SENSOR5_OPCODE, GET_SENSOR5);
    talks.bind(GET_SENSOR6_OPCODE, GET_SENSOR6);
    talks.bind(GET_SENSOR7_OPCODE, GET_SENSOR7);
    talks.bind(GET_SENSOR8_OPCODE, GET_SENSOR8);

    talks.bind(CHECK_ERROR_OPCODE, CHECK_ERROR);

    //bind subscription
    topics.bind(GET_ALL_OPCODE, GET_ALL);

    // Shutdown all VL53L0X sensors
    for (const auto &cur_sensor : sensors_vl53)
    {
        cur_sensor->shutdown();
    }

    // Set all VL53L0X timeout in ms
    for (const auto &cur_sensor : sensors_vl53)
    {
        cur_sensor->setTimeout(30);
    }

    // Starting all VL53L0X sensors
    for (const auto &cur_sensor : sensors_vl53)
    {
        if (!cur_sensor->begin())
        {
            vl53_status[count++] = 1;
        }
    }
    count = 0;

    // Starting all VL53L0X measure
    for (const auto &cur_sensor : sensors_vl53)
    {
        cur_sensor->startContinuous();
    }
}

// Loop
void loop()
{
    static uint16_t count = 0;

    talks.execute();
    topics.execute();

    for (const auto &cur_sensor : sensors_vl53)
    {
        vl53_measurement[count++] = cur_sensor->readRangeContinuousMillimeters(talksExecuteWrapper);
    }
    count = 0;
}