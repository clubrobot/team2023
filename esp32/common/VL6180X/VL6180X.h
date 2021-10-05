#ifndef __VL6180X_H
#define __VL6180X_H

#include <Arduino.h>
#include <Wire.h>
#include <ShiftRegister.h>
#include "VL6180X_Commons.h"

#define VL6180X_I2C_ADDR 0X29

class VL6180X
{
public:
    VL6180X(uint8_t i2c_addr = VL6180X_I2C_ADDR, uint8_t shutdown_pin = NULL, ShiftRegister *shift_reg = NULL, TwoWire *i2c = &Wire);

    void shutdown();
    bool begin();

    inline uint8_t get_last_status() { return _last_status; }
    inline uint8_t getAddress() { return _i2c_addr; }

    bool isInitialised() { return _init_state; }

    void configureDefault(void);

    void setScaling(uint8_t new_scaling);
    inline uint8_t getScaling(void) { return _scaling; }

    uint8_t readRangeSingle(void);
    inline uint16_t readRangeSingleMillimeters(void) { return (uint16_t)_scaling * readRangeSingle(); }
    uint16_t readAmbientSingle(void);

    void startRangeContinuous(uint16_t period = 100);
    void startAmbientContinuous(uint16_t period = 500);
    void startInterleavedContinuous(uint16_t period = 500);
    void stopContinuous();

    uint8_t readRangeContinuous(void);
    inline uint16_t readRangeContinuousMillimeters(void) { return (uint16_t)_scaling * readRangeContinuous(); }
    uint16_t readAmbientContinuous(void);

    inline void setTimeout(uint16_t timeout) { _io_timeout = timeout; }
    inline uint16_t getTimeout(void) { return _io_timeout; }
    bool timeoutOccurred(void);

private:
    void setAddress(uint8_t new_addr);

    void load_tunning_settings();

    void writeReg(uint16_t reg, uint8_t value);
    void writeReg16Bit(uint16_t reg, uint16_t value);
    void writeReg32Bit(uint16_t reg, uint32_t value);
    uint8_t readReg(uint16_t reg);
    uint16_t readReg16Bit(uint16_t reg);
    uint32_t readReg32Bit(uint16_t reg);

    uint8_t _i2c_addr;     // I2C device adress
    uint8_t _last_status;  // status of last I2C transmission
    uint8_t _shutdown_pin; // VL53L0X shutdown pin
    bool _init_state;      // initialisation status

    uint8_t _scaling;
    uint8_t _ptp_offset;
    uint16_t _io_timeout;
    uint16_t _previousRange = 65535;
    bool _did_timeout;

    TwoWire *_i2c;
    ShiftRegister *_shift_reg;
};

#endif
