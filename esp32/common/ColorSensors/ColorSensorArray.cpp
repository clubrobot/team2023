#include "ColorSensorArray.h"
#include <Arduino.h>


ColorSensorArray::ColorSensorArray() :
  mux_(nullptr),
  leds_pin_(-1),
  cup_color_estimate_sample_size_(10) {}

bool ColorSensorArray::set_channel(uint8_t channel) {
  // TODO: return actual value when mux hardware will be ready for testing.
  /*return*/ this->mux_->set_selected_channels(1 << (channel % 8)) == I2C_ERROR_OK;
  return true;
}

void ColorSensorArray::begin(TCA9548A *mux, uint8_t leds_pin) {
  this->mux_ = mux;
  this->leds_pin_ = leds_pin;
  pinMode(this->leds_pin_, OUTPUT);
  this->set_leds(LOW);
}

bool ColorSensorArray::begin(uint8_t channel) {
  if (!this->set_channel(channel)) {
    return false;
  }
  return this->sensor_interface_.begin(TCS34725_ADDRESS, this->mux_->get_wire());
}

void ColorSensorArray::reset() {
  this->mux_->reset();
}

bool ColorSensorArray::get_rgb(uint8_t channel, float *r, float *g, float *b) {
  if (!this->set_channel(channel)) {
    return false;
  }
  this->sensor_interface_.getRGB(r, g, b);
  return true;
}

bool ColorSensorArray::set_integration_time(uint8_t channel, tcs34725IntegrationTime_t it) {
  if (!this->set_channel(channel)) {
    return false;
  }
  this->sensor_interface_.setIntegrationTime(it);
  return true;
}

bool ColorSensorArray::set_gain(uint8_t channel, tcs34725Gain_t gain) {
  if (!this->set_channel(channel)) {
    return false;
  }
  this->sensor_interface_.setGain(gain);
  return true;
}

bool ColorSensorArray::enable(uint8_t channel) {
  if (!this->set_channel(channel)) {
    return false;
  }
  this->sensor_interface_.enable();
  return true;
}

bool ColorSensorArray::disable(uint8_t channel) {
  if (!this->set_channel(channel)) {
    return false;
  }
  this->sensor_interface_.disable();
  return true;
}

void ColorSensorArray::set_leds(uint8_t val) {
  digitalWrite(this->leds_pin_, val);
}

void ColorSensorArray::set_cup_color_estimate_sample_size(uint8_t sample_size) {
  if (sample_size == 0) {
    sample_size = 10;
  }
  this->cup_color_estimate_sample_size_ = sample_size;
}

ColorSensorArray::CupColorEstimate ColorSensorArray::get_cup_color_estimate(uint8_t channel) {
  if (!this->set_channel(channel)) {
    return COLOR_ESTIMATE_ERROR;
  }
  uint16_t sample_r = 0, sample_g = 0, sample_b = 0;
  float red, green, blue;

  this->set_leds(1);
  for (uint8_t i = 0; i < this->cup_color_estimate_sample_size_; i++) {
    this->sensor_interface_.getRGB(&red, &green, &blue);
    sample_r += int(red);
    sample_g += int(green);
    sample_b += int(blue);
  }
  this->set_leds(0);

  sample_r /= this->cup_color_estimate_sample_size_;
  sample_g /= this->cup_color_estimate_sample_size_;
  sample_b /= this->cup_color_estimate_sample_size_;

  if (sample_r > sample_g && sample_r > sample_b) {
    return COLOR_ESTIMATE_RED;
  } else if (sample_g > sample_r && sample_g > sample_b) {
    return COLOR_ESTIMATE_GREEN;
  } else {
    return COLOR_ESTIMATE_ERROR;
  }
}
