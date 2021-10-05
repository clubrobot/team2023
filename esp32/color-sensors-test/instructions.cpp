#include "instructions.h"

#include <SerialTalks.h>

void CSA_GET_CUP_COLOR_ESTIMATE(SerialTalks &inst, Deserializer &input, Serializer &output) {
  auto channel = input.read<uint8_t>();
  output.write<uint8_t>(color_sensor_array.get_cup_color_estimate(channel));
}

void CSA_GET_RGB(SerialTalks &inst, Deserializer &input, Serializer &output) {
  auto channel = input.read<uint8_t>();
  float red, green, blue;
  color_sensor_array.get_rgb(channel, &red, &green, &blue);
  output.write<float>(red);
  output.write<float>(green);
  output.write<float>(blue);
}

void CSA_SET_INTEGRATION_TIME(SerialTalks &inst, Deserializer &input, Serializer &output) {
  auto channel = input.read<uint8_t>();
  auto integration_time_code = input.read<uint8_t>();
  tcs34725IntegrationTime_t integration_time;
  switch (integration_time_code) {
    case 1:
      integration_time = TCS34725_INTEGRATIONTIME_24MS;
      break;
    case 2:
      integration_time = TCS34725_INTEGRATIONTIME_50MS;
      break;
    case 3:
      integration_time = TCS34725_INTEGRATIONTIME_101MS;
      break;
    case 4:
      integration_time = TCS34725_INTEGRATIONTIME_154MS;
      break;
    case 5:
      integration_time = TCS34725_INTEGRATIONTIME_700MS;
      break;
    default:
      integration_time = TCS34725_INTEGRATIONTIME_2_4MS;
      break;
  }
  color_sensor_array.set_integration_time(channel, integration_time);
}

void CSA_SET_GAIN(SerialTalks &inst, Deserializer &input, Serializer &output) {
  auto channel = input.read<uint8_t>();
  auto gain_code = input.read<uint8_t>();
  tcs34725Gain_t gain;
  switch (gain_code) {
    case 1:
      gain = TCS34725_GAIN_4X;
      break;
    case 2:
      gain = TCS34725_GAIN_16X;
      break;
    case 3:
      gain = TCS34725_GAIN_60X;
      break;
    default:
      gain = TCS34725_GAIN_1X;
      break;
  }
  color_sensor_array.set_gain(channel, gain);
}

void CSA_ENABLE(SerialTalks &inst, Deserializer &input, Serializer &output) {
  auto channel = input.read<uint8_t>();
  color_sensor_array.enable(channel);
}

void CSA_DISABLE(SerialTalks &inst, Deserializer &input, Serializer &output) {
  auto channel = input.read<uint8_t>();
  color_sensor_array.disable(channel);
}

void CSA_LEDS_ON(SerialTalks &inst, Deserializer &input, Serializer &output) {
  color_sensor_array.set_leds(HIGH);
}

void CSA_LEDS_OFF(SerialTalks &inst, Deserializer &input, Serializer &output) {
  color_sensor_array.set_leds(LOW);
}

void CSA_SET_CUP_COLOR_ESTIMATE_SAMPLE_SIZE(SerialTalks &inst, Deserializer &input, Serializer &output) {
  auto sample_size = input.read<uint8_t>();
  color_sensor_array.set_cup_color_estimate_sample_size(sample_size);
}

void CSA_RESET(SerialTalks &inst, Deserializer &input, Serializer &output) {
  color_sensor_array.reset();
}
