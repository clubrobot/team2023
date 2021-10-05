#include "TCA9548A.h"

TCA9548A::TCA9548A() : address_(TCA9548A_DEFAULT_ADDRESS), reset_pin_(-1), wire_(nullptr) {
}

bool TCA9548A::begin(uint8_t reset_pin, uint8_t address, TwoWire *wire) {
  this->wire_ = wire;
  this->reset_pin_ = reset_pin;
  this->address_ = address;
  pinMode(this->reset_pin_, OUTPUT);
  this->reset();
  return this->wire_->requestFrom(this->address_, 1u) != 0;
}

uint8_t TCA9548A::get_selected_channels(uint8_t *channels) const {
  if (this->wire_->requestFrom(this->address_, 1u) == 0) {
    return this->wire_->lastError() == I2C_ERROR_OK ? I2C_ERROR_DEV : this->wire_->lastError();
  }
  *channels = this->wire_->read();
  return I2C_ERROR_OK;
}

uint8_t TCA9548A::set_selected_channels(uint8_t channels) {
  this->wire_->beginTransmission(this->address_);
  this->wire_->write(channels);
  return this->wire_->endTransmission();
}

TwoWire *TCA9548A::get_wire() {
  return this->wire_;
}

void TCA9548A::reset() {
  digitalWrite(this->reset_pin_, LOW);
  delayMicroseconds(1);
  digitalWrite(this->reset_pin_, HIGH);
}
