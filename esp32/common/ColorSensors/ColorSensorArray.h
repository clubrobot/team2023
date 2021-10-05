#ifndef _COLOR_SENSOR_ARRAY_
#define _COLOR_SENSOR_ARRAY_

#include <TCA9548A.h>
#include <Adafruit_TCS34725.h>

class ColorSensorArray {
  protected:
  Adafruit_TCS34725 sensor_interface_;
  TCA9548A *mux_;
  uint8_t leds_pin_;
  uint8_t cup_color_estimate_sample_size_;

  bool set_channel(uint8_t channel);

  public:
  ColorSensorArray();

  enum CupColorEstimate {
    COLOR_ESTIMATE_RED,
    COLOR_ESTIMATE_GREEN,
    COLOR_ESTIMATE_ERROR
  };

  void begin(TCA9548A *mux, uint8_t leds_pin);
  bool begin(uint8_t channel);
  void reset();

  bool get_rgb(uint8_t channel, float *r, float *g, float *b);
  bool set_integration_time(uint8_t channel, tcs34725IntegrationTime_t it);
  bool set_gain(uint8_t channel, tcs34725Gain_t gain);
  bool enable(uint8_t channel);
  bool disable(uint8_t channel);
  void set_leds(uint8_t val);
  void set_cup_color_estimate_sample_size(uint8_t sample_size);
  CupColorEstimate get_cup_color_estimate(uint8_t channel);
};

#endif // _COLOR_SENSOR_ARRAY_
