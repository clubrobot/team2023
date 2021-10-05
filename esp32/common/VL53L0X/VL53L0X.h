#ifndef __VL53L0X_H
#define __VL53L0X_H

#include <Arduino.h>
#include <Wire.h>
#include <ShiftRegister.h>
#include "VL53L0X_Commons.h"

#define VL53L0X_I2C_ADDR 0X29

class VL53L0X
{
public:
    VL53L0X(uint8_t i2c_addr = VL53L0X_I2C_ADDR, uint8_t shutdown_pin = NULL, ShiftRegister *shift_reg = NULL, TwoWire *i2c = &Wire);

    void shutdown();
    bool begin(bool io_2v8 = true);

    bool isInitialised() { return _init_state; }

    inline uint8_t get_last_status() { return _last_status; }

    inline uint8_t getAddress() { return _i2c_addr; }

    bool setSignalRateLimit(float limit_Mcps);
    float getSignalRateLimit();

    bool setMeasurementTimingBudget(uint32_t budget_us);
    uint32_t getMeasurementTimingBudget();

    bool setVcselPulsePeriod(VL53L0X_VcselPeriodType_t type, uint8_t period_pclks);
    uint8_t getVcselPulsePeriod(VL53L0X_VcselPeriodType_t type);

    void startContinuous(uint32_t period_ms = 0);
    void stopContinuous();
    uint16_t readRangeContinuousMillimeters(void (*functionPointer)());

    inline void setTimeout(uint16_t timeout) { _io_timeout = timeout; }
    inline uint16_t getTimeout() { return _io_timeout; }

    bool timeoutOccurred();

private:
    void setAddress(uint8_t new_addr);

    void load_tunning_settings();

    void writeReg(uint8_t reg, uint8_t value);
    void writeReg16Bit(uint8_t reg, uint16_t value);
    void writeReg32Bit(uint8_t reg, uint32_t value);

    uint8_t readReg(uint8_t reg);
    uint16_t readReg16Bit(uint8_t reg);
    uint32_t readReg32Bit(uint8_t reg);

    void writeMulti(uint8_t reg, uint8_t const *src, uint8_t count);
    void readMulti(uint8_t reg, uint8_t *dst, uint8_t count);

    struct SequenceStepEnables
    {
        bool tcc, msrc, dss, pre_range, final_range;
    };

    struct SequenceStepTimeouts
    {
        uint16_t pre_range_vcsel_period_pclks, final_range_vcsel_period_pclks;

        uint16_t msrc_dss_tcc_mclks, pre_range_mclks, final_range_mclks;
        uint32_t msrc_dss_tcc_us, pre_range_us, final_range_us;
    };

    bool getSpadInfo(uint8_t *count, bool *type_is_aperture);

    void getSequenceStepEnables(SequenceStepEnables *enables);
    void getSequenceStepTimeouts(SequenceStepEnables const *enables, SequenceStepTimeouts *timeouts);

    bool performSingleRefCalibration(uint8_t vhv_init_byte);

    static uint16_t decodeTimeout(uint16_t value);
    static uint16_t encodeTimeout(uint16_t timeout_mclks);
    static uint32_t timeoutMclksToMicroseconds(uint16_t timeout_period_mclks, uint8_t vcsel_period_pclks);
    static uint32_t timeoutMicrosecondsToMclks(uint32_t timeout_period_us, uint8_t vcsel_period_pclks);

    uint8_t _i2c_addr;     // I2C device adress
    uint8_t _last_status;  // status of last I2C transmission
    uint8_t _shutdown_pin; // VL53L0X shutdown pin
    bool _init_state;      // initialisation status

    uint16_t _io_timeout;
    bool _did_timeout;
    uint16_t _timeout_start_ms;

    uint8_t _stop_variable; // read by init and used when starting measurement; is StopVariable field of VL53L0X_DevData_t structure in API
    uint32_t _measurement_timing_budget_us;

    uint16_t _previousRange = 65535;

    TwoWire *_i2c;
    ShiftRegister *_shift_reg;
};

#endif /* __VL53L0X_H */