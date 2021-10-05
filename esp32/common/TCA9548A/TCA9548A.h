#ifndef _TCA9548A_H_
#define _TCA9548A_H_

#include <Wire.h>

#define TCA9548A_DEFAULT_ADDRESS 0x70

class TCA9548A {
  protected:
  uint8_t address_;
  uint8_t reset_pin_;
  TwoWire *wire_;
  public:
  TCA9548A();

  /**
   * Initialises the multiplexer with its 7 bit address. The first 4 bits are
   * always 1110, the 3 remaining are hardware selectable using the A2, A1 and
   * A0 pins.
   */
  bool begin(uint8_t reset_pin, uint8_t address = TCA9548A_DEFAULT_ADDRESS, TwoWire *wire = &Wire);
  uint8_t get_selected_channels(uint8_t *channels) const;
  uint8_t set_selected_channels(uint8_t channels);
  TwoWire *get_wire();

  /**
   * Resets the multiplexer by lowering the reset pin.
   */
  void reset();
};

#endif // _TCA9548A_H_
