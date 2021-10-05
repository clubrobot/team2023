#include <Arduino.h>

#include <SerialTalks.h>
#include <ColorSensorArray.h>

#include "instructions.h"

TCA9548A color_sensor_array_mux;
ColorSensorArray color_sensor_array;

void setup()
{
  // Communication
  Serial.begin(SERIALTALKS_BAUDRATE);
  talks.begin(Serial);

  if (!color_sensor_array_mux.begin(34)) {
    // !ERROR.
  }
  color_sensor_array.begin(&color_sensor_array_mux, 23);
  if (!color_sensor_array.begin(0)) {
    // !ERROR.
  }

  // bind functions
  talks.bind(CSA_GET_CUP_COLOR_ESTIMATE_OPCODE, CSA_GET_CUP_COLOR_ESTIMATE);
  talks.bind(CSA_GET_RGB_OPCODE, CSA_GET_RGB);
  talks.bind(CSA_SET_INTEGRATION_TIME_OPCODE, CSA_SET_INTEGRATION_TIME);
  talks.bind(CSA_SET_GAIN_OPCODE, CSA_SET_GAIN);
  talks.bind(CSA_ENABLE_OPCODE, CSA_ENABLE);
  talks.bind(CSA_DISABLE_OPCODE, CSA_DISABLE);
  talks.bind(CSA_LEDS_ON_OPCODE, CSA_LEDS_ON);
  talks.bind(CSA_LEDS_OFF_OPCODE, CSA_LEDS_OFF);
  talks.bind(CSA_SET_CUP_COLOR_ESTIMATE_SAMPLE_SIZE_OPCODE, CSA_SET_CUP_COLOR_ESTIMATE_SAMPLE_SIZE);
  talks.bind(CSA_RESET_OPCODE, CSA_RESET);
}

void loop()
{
  talks.execute();
}
