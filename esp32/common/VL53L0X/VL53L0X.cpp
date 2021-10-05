#include "VL53L0X.h"
#include "VL53L0X_tuning.h"

/*  Record the current time to check an upcoming timeout against*/
#define startTimeout() (_timeout_start_ms = millis())

/*  Check if timeout is enabled (set to nonzero value) and has expired*/
#define checkTimeoutExpired() (_io_timeout > 0 && ((uint16_t)millis() - _timeout_start_ms) > _io_timeout)

/*  Decode VCSEL (vertical cavity surface emitting laser) pulse period in PCLKs
    from register value
    based on VL53L0X_decode_vcsel_period() */
#define decodeVcselPeriod(reg_val) (((reg_val) + 1) << 1)

/*  Encode VCSEL pulse period register value from period in PCLKs
    based on VL53L0X_encode_vcsel_period() */
#define encodeVcselPeriod(period_pclks) (((period_pclks) >> 1) - 1)

/*  Calculate macro period in *nanoseconds* from VCSEL period in PCLKs
    based on VL53L0X_calc_macro_period_ps()
    PLL_period_ps = 1655; macro_period_vclks = 2304 */
#define calcMacroPeriod(vcsel_period_pclks) ((((uint32_t)2304 * (vcsel_period_pclks)*1655) + 500) / 1000)

VL53L0X::VL53L0X(uint8_t i2c_addr, uint8_t shutdown_pin, ShiftRegister *shift_reg, TwoWire *i2c)
    : _i2c_addr(i2c_addr), _shutdown_pin(shutdown_pin), _shift_reg(shift_reg), _i2c(i2c)
{
    _io_timeout = 0;
    _did_timeout = false;
    _init_state = false;
}

void VL53L0X::shutdown()
{
    /* always shutdown the sensor at the beggining */
    if (_shift_reg != NULL)
    {
        _shift_reg->SetLow(_shutdown_pin);
    }
    else
    {
        if (_shutdown_pin != NULL)
        {
            pinMode(_shutdown_pin, OUTPUT);
            digitalWrite(_shutdown_pin, LOW);
        }
    }
}

bool VL53L0X::begin(bool io_2v8)
{
    uint8_t spad_count;
    bool spad_type_is_aperture;

    /* enable the sensor */
    if (_shift_reg != NULL)
    {
        _shift_reg->SetHigh(_shutdown_pin);
        delay(2);
    }
    else
    {
        if (_shutdown_pin != NULL)
        {
            digitalWrite(_shutdown_pin, HIGH);
            delay(2);
        }
    }

    /* set its own adress */
    setAddress(_i2c_addr);

    /* sensor uses 1V8 mode for I/O by default; switch to 2V8 mode if necessary */
    if (io_2v8)
    {
        writeReg(VL53L0X_VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV, readReg(VL53L0X_VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV) | 0x01);
    }

    /* "Set I2C standard mode" */
    writeReg(0x88, 0x00);

    writeReg(0x80, 0x01);
    writeReg(0xFF, 0x01);
    writeReg(0x00, 0x00);
    _stop_variable = readReg(0x91);
    writeReg(0x00, 0x01);
    writeReg(0xFF, 0x00);
    writeReg(0x80, 0x00);

    // disable SIGNAL_RATE_MSRC (bit 1) and SIGNAL_RATE_PRE_RANGE (bit 4) limit checks
    writeReg(VL53L0X_MSRC_CONFIG_CONTROL, readReg(VL53L0X_MSRC_CONFIG_CONTROL) | 0x12);

    /* set final range signal rate limit to 0.25 MCPS (million counts per second) */
    setSignalRateLimit(0.25);

    writeReg(VL53L0X_SYSTEM_SEQUENCE_CONFIG, 0xFF);

    if (!getSpadInfo(&spad_count, &spad_type_is_aperture))
    {
        return false;
    }

    /*  The SPAD map (RefGoodSpadMap) is read by VL53L0X_get_info_from_device() in
        the API, but the same data seems to be more easily readable from
        GLOBAL_CONFIG_SPAD_ENABLES_REF_0 through _6, so read it from there */
    uint8_t ref_spad_map[6];
    readMulti(VL53L0X_GLOBAL_CONFIG_SPAD_ENABLES_REF_0, ref_spad_map, 6);

    /* -- VL53L0X_set_reference_spads() begin (assume NVM values are valid) */

    writeReg(VL53L0X_REG_MAX, 0x01);
    writeReg(VL53L0X_DYNAMIC_SPAD_REF_EN_START_OFFSET, 0x00);
    writeReg(VL53L0X_DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD, 0x2C);
    writeReg(VL53L0X_REG_MAX, 0x00);
    writeReg(VL53L0X_GLOBAL_CONFIG_REF_EN_START_SELECT, 0xB4);

    uint8_t first_spad_to_enable = spad_type_is_aperture ? 12 : 0; /* 12 is the first aperture spad */
    uint8_t spads_enabled = 0;

    for (uint8_t i = 0; i < 48; i++)
    {
        if (i < first_spad_to_enable || spads_enabled == spad_count)
        {
            /*  This bit is lower than the first one that should be enabled, or
                (reference_spad_count) bits have already been enabled, so zero this bit */
            ref_spad_map[i / 8] &= ~(1 << (i % 8));
        }
        else if ((ref_spad_map[i / 8] >> (i % 8)) & 0x1)
        {
            spads_enabled++;
        }
    }

    writeMulti(VL53L0X_GLOBAL_CONFIG_SPAD_ENABLES_REF_0, ref_spad_map, 6);

    /* load tuning register */
    load_tunning_settings();

    /*  "Set interrupt config to new sample ready" */
    writeReg(VL53L0X_SYSTEM_INTERRUPT_CONFIG_GPIO, 0x04);
    writeReg(VL53L0X_GPIO_HV_MUX_ACTIVE_HIGH, readReg(VL53L0X_GPIO_HV_MUX_ACTIVE_HIGH) & ~0x10); // active low
    writeReg(VL53L0X_SYSTEM_INTERRUPT_CLEAR, 0x01);

    _measurement_timing_budget_us = getMeasurementTimingBudget();

    /*  "Disable MSRC and TCC by default"
        MSRC = Minimum Signal Rate Check
        TCC = Target CentreCheck */

    writeReg(VL53L0X_SYSTEM_SEQUENCE_CONFIG, 0xE8);

    /* "Recalculate timing budget" */
    setMeasurementTimingBudget(_measurement_timing_budget_us);

    writeReg(VL53L0X_SYSTEM_SEQUENCE_CONFIG, 0x01);
    if (!performSingleRefCalibration(0x40))
    {
        return false;
    }

    writeReg(VL53L0X_SYSTEM_SEQUENCE_CONFIG, 0x02);
    if (!performSingleRefCalibration(0x00))
    {
        return false;
    }

    /* "restore the previous Sequence Config" */
    writeReg(VL53L0X_SYSTEM_SEQUENCE_CONFIG, 0xE8);

    _init_state = true;

    return true;
}

bool VL53L0X::setSignalRateLimit(float limit_Mcps)
{
    if (limit_Mcps < 0 || limit_Mcps > 511.99)
    {
        return false;
    }

    /* Q9.7 fixed point format (9 integer bits, 7 fractional bits) */
    writeReg16Bit(VL53L0X_FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT, limit_Mcps * (1 << 7));
    return true;
}

bool VL53L0X::setMeasurementTimingBudget(uint32_t budget_us)
{
    SequenceStepEnables enables;
    SequenceStepTimeouts timeouts;

    uint16_t const StartOverhead = 1320; /* note that this is different than the value in get_ */
    uint16_t const EndOverhead = 960;
    uint16_t const MsrcOverhead = 660;
    uint16_t const TccOverhead = 590;
    uint16_t const DssOverhead = 690;
    uint16_t const PreRangeOverhead = 660;
    uint16_t const FinalRangeOverhead = 550;

    uint32_t const MinTimingBudget = 20000;

    if (budget_us < MinTimingBudget)
    {
        return false;
    }

    uint32_t used_budget_us = StartOverhead + EndOverhead;

    getSequenceStepEnables(&enables);
    getSequenceStepTimeouts(&enables, &timeouts);

    if (enables.tcc)
    {
        used_budget_us += (timeouts.msrc_dss_tcc_us + TccOverhead);
    }

    if (enables.dss)
    {
        used_budget_us += 2 * (timeouts.msrc_dss_tcc_us + DssOverhead);
    }
    else if (enables.msrc)
    {
        used_budget_us += (timeouts.msrc_dss_tcc_us + MsrcOverhead);
    }

    if (enables.pre_range)
    {
        used_budget_us += (timeouts.pre_range_us + PreRangeOverhead);
    }

    if (enables.final_range)
    {
        used_budget_us += FinalRangeOverhead;

        /*  "Note that the final range timeout is determined by the timing
            budget and the sum of all other timeouts within the sequence.
            If there is no room for the final range timeout, then an error
            will be set. Otherwise the remaining time will be applied to
            the final range." */

        if (used_budget_us > budget_us)
        {
            /* "Requested timeout too big."*/
            return false;
        }

        uint32_t final_range_timeout_us = budget_us - used_budget_us;

        /*  "For the final range timeout, the pre-range timeout
            must be added. To do this both final and pre-range
            timeouts must be expressed in macro periods MClks
            because they have different vcsel periods." */

        uint16_t final_range_timeout_mclks = timeoutMicrosecondsToMclks(final_range_timeout_us, timeouts.final_range_vcsel_period_pclks);

        if (enables.pre_range)
        {
            final_range_timeout_mclks += timeouts.pre_range_mclks;
        }

        writeReg16Bit(VL53L0X_FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI, encodeTimeout(final_range_timeout_mclks));

        _measurement_timing_budget_us = budget_us; // store for internal reuse
    }
    return true;
}

uint32_t VL53L0X::getMeasurementTimingBudget()
{
    SequenceStepEnables enables;
    SequenceStepTimeouts timeouts;

    uint16_t const StartOverhead = 1910; // note that this is different than the value in set_
    uint16_t const EndOverhead = 960;
    uint16_t const MsrcOverhead = 660;
    uint16_t const TccOverhead = 590;
    uint16_t const DssOverhead = 690;
    uint16_t const PreRangeOverhead = 660;
    uint16_t const FinalRangeOverhead = 550;

    /* "Start and end overhead times always present" */
    uint32_t budget_us = StartOverhead + EndOverhead;

    getSequenceStepEnables(&enables);
    getSequenceStepTimeouts(&enables, &timeouts);

    if (enables.tcc)
    {
        budget_us += (timeouts.msrc_dss_tcc_us + TccOverhead);
    }

    if (enables.dss)
    {
        budget_us += 2 * (timeouts.msrc_dss_tcc_us + DssOverhead);
    }
    else if (enables.msrc)
    {
        budget_us += (timeouts.msrc_dss_tcc_us + MsrcOverhead);
    }

    if (enables.pre_range)
    {
        budget_us += (timeouts.pre_range_us + PreRangeOverhead);
    }

    if (enables.final_range)
    {
        budget_us += (timeouts.final_range_us + FinalRangeOverhead);
    }

    _measurement_timing_budget_us = budget_us; /* store for internal reuse */
    return budget_us;
}

bool VL53L0X::setVcselPulsePeriod(VL53L0X_VcselPeriodType_t type, uint8_t period_pclks)
{
    uint8_t vcsel_period_reg = encodeVcselPeriod(period_pclks);

    SequenceStepEnables enables;
    SequenceStepTimeouts timeouts;

    getSequenceStepEnables(&enables);
    getSequenceStepTimeouts(&enables, &timeouts);

    /*  "Apply specific settings for the requested clock period"
        "Re-calculate and apply timeouts, in macro periods"

        "When the VCSEL period for the pre or final range is changed,
        the corresponding timeout must be read from the device using
        the current VCSEL period, then the new VCSEL period can be
        applied. The timeout then must be written back to the device
        using the new VCSEL period.

        For the MSRC timeout, the same applies - this timeout being
        dependant on the pre-range vcsel period." */

    if (type == VcselPeriodPreRange)
    {
        /* "Set phase check limits" */
        switch (period_pclks)
        {
        case 12:
            writeReg(VL53L0X_PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x18);
            break;

        case 14:
            writeReg(VL53L0X_PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x30);
            break;

        case 16:
            writeReg(VL53L0X_PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x40);
            break;

        case 18:
            writeReg(VL53L0X_PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x50);
            break;

        default:
            /* invalid period */
            return false;
        }
        writeReg(VL53L0X_PRE_RANGE_CONFIG_VALID_PHASE_LOW, 0x08);

        /* apply new VCSEL period */
        writeReg(VL53L0X_PRE_RANGE_CONFIG_VCSEL_PERIOD, vcsel_period_reg);

        uint16_t new_pre_range_timeout_mclks = timeoutMicrosecondsToMclks(timeouts.pre_range_us, period_pclks);

        writeReg16Bit(VL53L0X_PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI, encodeTimeout(new_pre_range_timeout_mclks));

        uint16_t new_msrc_timeout_mclks = timeoutMicrosecondsToMclks(timeouts.msrc_dss_tcc_us, period_pclks);

        writeReg(VL53L0X_MSRC_CONFIG_TIMEOUT_MACROP, (new_msrc_timeout_mclks > 256) ? 255 : (new_msrc_timeout_mclks - 1));
    }
    else if (type == VcselPeriodFinalRange)
    {
        switch (period_pclks)
        {
        case 8:
            writeReg(VL53L0X_FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x10);
            writeReg(VL53L0X_FINAL_RANGE_CONFIG_VALID_PHASE_LOW, 0x08);
            writeReg(VL53L0X_GLOBAL_CONFIG_VCSEL_WIDTH, 0x02);
            writeReg(VL53L0X_ALGO_PHASECAL_CONFIG_TIMEOUT, 0x0C);
            writeReg(0xFF, 0x01);
            writeReg(VL53L0X_ALGO_PHASECAL_LIM, 0x30);
            writeReg(0xFF, 0x00);
            break;

        case 10:
            writeReg(VL53L0X_FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x28);
            writeReg(VL53L0X_FINAL_RANGE_CONFIG_VALID_PHASE_LOW, 0x08);
            writeReg(VL53L0X_GLOBAL_CONFIG_VCSEL_WIDTH, 0x03);
            writeReg(VL53L0X_ALGO_PHASECAL_CONFIG_TIMEOUT, 0x09);
            writeReg(0xFF, 0x01);
            writeReg(VL53L0X_ALGO_PHASECAL_LIM, 0x20);
            writeReg(0xFF, 0x00);
            break;

        case 12:
            writeReg(VL53L0X_FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x38);
            writeReg(VL53L0X_FINAL_RANGE_CONFIG_VALID_PHASE_LOW, 0x08);
            writeReg(VL53L0X_GLOBAL_CONFIG_VCSEL_WIDTH, 0x03);
            writeReg(VL53L0X_ALGO_PHASECAL_CONFIG_TIMEOUT, 0x08);
            writeReg(0xFF, 0x01);
            writeReg(VL53L0X_ALGO_PHASECAL_LIM, 0x20);
            writeReg(0xFF, 0x00);
            break;

        case 14:
            writeReg(VL53L0X_FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x48);
            writeReg(VL53L0X_FINAL_RANGE_CONFIG_VALID_PHASE_LOW, 0x08);
            writeReg(VL53L0X_GLOBAL_CONFIG_VCSEL_WIDTH, 0x03);
            writeReg(VL53L0X_ALGO_PHASECAL_CONFIG_TIMEOUT, 0x07);
            writeReg(0xFF, 0x01);
            writeReg(VL53L0X_ALGO_PHASECAL_LIM, 0x20);
            writeReg(0xFF, 0x00);
            break;

        default:
            /* invalid period */
            return false;
        }

        /* apply new VCSEL period */
        writeReg(VL53L0X_FINAL_RANGE_CONFIG_VCSEL_PERIOD, vcsel_period_reg);

        /*  "For the final range timeout, the pre-range timeout
            must be added. To do this both final and pre-range
            timeouts must be expressed in macro periods MClks
            because they have different vcsel periods." */

        uint16_t new_final_range_timeout_mclks = timeoutMicrosecondsToMclks(timeouts.final_range_us, period_pclks);

        if (enables.pre_range)
        {
            new_final_range_timeout_mclks += timeouts.pre_range_mclks;
        }

        writeReg16Bit(VL53L0X_FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI, encodeTimeout(new_final_range_timeout_mclks));
    }
    else
    {
        /* invalid type */
        return false;
    }

    /*  "Finally, the timing budget must be re-applied" */
    setMeasurementTimingBudget(_measurement_timing_budget_us);

    /*  "Perform the phase calibration. This is needed after changing on vcsel period." */

    uint8_t sequence_config = readReg(VL53L0X_SYSTEM_SEQUENCE_CONFIG);
    writeReg(VL53L0X_SYSTEM_SEQUENCE_CONFIG, 0x02);
    performSingleRefCalibration(0x0);
    writeReg(VL53L0X_SYSTEM_SEQUENCE_CONFIG, sequence_config);

    return true;
}

uint8_t VL53L0X::getVcselPulsePeriod(VL53L0X_VcselPeriodType_t type)
{
    if (type == VcselPeriodPreRange)
    {
        return decodeVcselPeriod(readReg(VL53L0X_PRE_RANGE_CONFIG_VCSEL_PERIOD));
    }
    else if (type == VcselPeriodFinalRange)
    {
        return decodeVcselPeriod(readReg(VL53L0X_FINAL_RANGE_CONFIG_VCSEL_PERIOD));
    }
    else
    {
        return 255;
    }
}

void VL53L0X::startContinuous(uint32_t period_ms)
{
    writeReg(0x80, 0x01);
    writeReg(0xFF, 0x01);
    writeReg(0x00, 0x00);
    writeReg(0x91, _stop_variable);
    writeReg(0x00, 0x01);
    writeReg(0xFF, 0x00);
    writeReg(0x80, 0x00);

    if (period_ms != 0)
    {
        /* continuous timed mode */

        uint16_t osc_calibrate_val = readReg16Bit(VL53L0X_OSC_CALIBRATE_VAL);

        if (osc_calibrate_val != 0)
        {
            period_ms *= osc_calibrate_val;
        }

        writeReg32Bit(VL53L0X_SYSTEM_INTERMEASUREMENT_PERIOD, period_ms);

        writeReg(VL53L0X_SYSRANGE_START, 0x04);
    }
    else
    {
        /* continuous back-to-back mode */
        writeReg(VL53L0X_SYSRANGE_START, 0x02);
    }
}

void VL53L0X::stopContinuous()
{
    writeReg(VL53L0X_SYSRANGE_START, 0x01);

    writeReg(0xFF, 0x01);
    writeReg(0x00, 0x00);
    writeReg(0x91, 0x00);
    writeReg(0x00, 0x01);
    writeReg(0xFF, 0x00);
}

uint16_t VL53L0X::readRangeContinuousMillimeters(void (*functionPointer)())
{
    while ((readReg(VL53L0X_RESULT_INTERRUPT_STATUS) & 0x07) == 0)
    {
        if (checkTimeoutExpired())
        {
            _did_timeout = true;
            return _previousRange;
        }
        if (functionPointer != NULL)
        {
            functionPointer();
        }
    }
    /*  assumptions: Linearity Corrective Gain is 1000 (default);
        fractional ranging is not enabled*/

    uint16_t range = readReg16Bit(VL53L0X_RESULT_RANGE_STATUS + 10);

    writeReg(VL53L0X_SYSTEM_INTERRUPT_CLEAR, 0x01);

    _previousRange = range;

    return range;
}

bool VL53L0X::timeoutOccurred()
{
    bool tmp = _did_timeout;
    _did_timeout = false;
    return tmp;
}

float VL53L0X::getSignalRateLimit()
{
    return (float)readReg16Bit(VL53L0X_FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT) / (1 << 7);
}

void VL53L0X::setAddress(uint8_t new_addr)
{
    _i2c->beginTransmission(VL53L0X_I2C_ADDR);
    _i2c->write(VL53L0X_I2C_SLAVE_DEVICE_ADDRESS);
    _i2c->write(new_addr & 0x7F);
    _last_status = _i2c->endTransmission();
}

void VL53L0X::load_tunning_settings()
{
    for (unsigned int i = 0; i < (sizeof(VL53L0X_tuning_table) / sizeof(VL53L0X_tuning_t)); i++)
    {
        writeReg(VL53L0X_tuning_table[i].reg, VL53L0X_tuning_table[i].value);
    }
}

// Write an 8-bit register
void VL53L0X::writeReg(uint8_t reg, uint8_t value)
{
    _i2c->beginTransmission(_i2c_addr);
    _i2c->write(reg);
    _i2c->write(value);
    _last_status = _i2c->endTransmission();
}

// Write a 16-bit register
void VL53L0X::writeReg16Bit(uint8_t reg, uint16_t value)
{
    _i2c->beginTransmission(_i2c_addr);
    _i2c->write(reg);
    _i2c->write((value >> 8) & 0xFF); // value high byte
    _i2c->write(value & 0xFF);        // value low byte
    _last_status = _i2c->endTransmission();
}

// Write a 32-bit register
void VL53L0X::writeReg32Bit(uint8_t reg, uint32_t value)
{
    _i2c->beginTransmission(_i2c_addr);
    _i2c->write(reg);
    _i2c->write((value >> 24) & 0xFF); // value highest byte
    _i2c->write((value >> 16) & 0xFF);
    _i2c->write((value >> 8) & 0xFF);
    _i2c->write(value & 0xFF); // value lowest byte
    _last_status = _i2c->endTransmission();
}

// Read an 8-bit register
uint8_t VL53L0X::readReg(uint8_t reg)
{
    uint8_t value;

    _i2c->beginTransmission(_i2c_addr);
    _i2c->write(reg);
    _last_status = _i2c->endTransmission();

    _i2c->requestFrom(_i2c_addr, (uint8_t)1);
    value = _i2c->read();

    return value;
}

// Read a 16-bit register
uint16_t VL53L0X::readReg16Bit(uint8_t reg)
{
    uint16_t value;

    _i2c->beginTransmission(_i2c_addr);
    _i2c->write(reg);
    _last_status = _i2c->endTransmission();

    _i2c->requestFrom(_i2c_addr, (uint8_t)2);
    value = (uint16_t)_i2c->read() << 8; // value high byte
    value |= _i2c->read();               // value low byte

    return value;
}

// Read a 32-bit register
uint32_t VL53L0X::readReg32Bit(uint8_t reg)
{
    uint32_t value;

    _i2c->beginTransmission(_i2c_addr);
    _i2c->write(reg);
    _last_status = _i2c->endTransmission();

    _i2c->requestFrom(_i2c_addr, (uint8_t)4);
    value = (uint32_t)_i2c->read() << 24; // value highest byte
    value |= (uint32_t)_i2c->read() << 16;
    value |= (uint16_t)_i2c->read() << 8;
    value |= _i2c->read(); // value lowest byte

    return value;
}

// Write an arbitrary number of bytes from the given array to the sensor,
// starting at the given register
void VL53L0X::writeMulti(uint8_t reg, uint8_t const *src, uint8_t count)
{
    _i2c->beginTransmission(_i2c_addr);
    _i2c->write(reg);

    while (count-- > 0)
    {
        _i2c->write(*(src++));
    }

    _last_status = _i2c->endTransmission();
}

// Read an arbitrary number of bytes from the sensor, starting at the given
// register, into the given array
void VL53L0X::readMulti(uint8_t reg, uint8_t *dst, uint8_t count)
{
    _i2c->beginTransmission(_i2c_addr);
    _i2c->write(reg);
    _last_status = _i2c->endTransmission();

    _i2c->requestFrom(_i2c_addr, count);

    while (count-- > 0)
    {
        *(dst++) = _i2c->read();
    }
}

bool VL53L0X::getSpadInfo(uint8_t *count, bool *type_is_aperture)
{
    uint8_t tmp;

    writeReg(0x80, 0x01);
    writeReg(0xFF, 0x01);
    writeReg(0x00, 0x00);

    writeReg(0xFF, 0x06);
    writeReg(0x83, readReg(0x83) | 0x04);
    writeReg(0xFF, 0x07);
    writeReg(0x81, 0x01);

    writeReg(0x80, 0x01);

    writeReg(0x94, 0x6b);
    writeReg(0x83, 0x00);
    startTimeout();
    while (readReg(0x83) == 0x00)
    {
        if (checkTimeoutExpired())
        {
            return false;
        }
    }
    writeReg(0x83, 0x01);
    tmp = readReg(0x92);

    *count = tmp & 0x7f;
    *type_is_aperture = (tmp >> 7) & 0x01;

    writeReg(0x81, 0x00);
    writeReg(0xFF, 0x06);
    writeReg(0x83, readReg(0x83) & ~0x04);
    writeReg(0xFF, 0x01);
    writeReg(0x00, 0x01);

    writeReg(0xFF, 0x00);
    writeReg(0x80, 0x00);

    return true;
}

void VL53L0X::getSequenceStepEnables(SequenceStepEnables *enables)
{
    uint8_t sequence_config = readReg(VL53L0X_SYSTEM_SEQUENCE_CONFIG);

    enables->tcc = (sequence_config >> 4) & 0x1;
    enables->dss = (sequence_config >> 3) & 0x1;
    enables->msrc = (sequence_config >> 2) & 0x1;
    enables->pre_range = (sequence_config >> 6) & 0x1;
    enables->final_range = (sequence_config >> 7) & 0x1;
}

void VL53L0X::getSequenceStepTimeouts(SequenceStepEnables const *enables, SequenceStepTimeouts *timeouts)
{
    timeouts->pre_range_vcsel_period_pclks = getVcselPulsePeriod(VcselPeriodPreRange);

    timeouts->msrc_dss_tcc_mclks = readReg(VL53L0X_MSRC_CONFIG_TIMEOUT_MACROP) + 1;
    timeouts->msrc_dss_tcc_us = timeoutMclksToMicroseconds(timeouts->msrc_dss_tcc_mclks, timeouts->pre_range_vcsel_period_pclks);

    timeouts->pre_range_mclks = decodeTimeout(readReg16Bit(VL53L0X_PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI));
    timeouts->pre_range_us = timeoutMclksToMicroseconds(timeouts->pre_range_mclks, timeouts->pre_range_vcsel_period_pclks);

    timeouts->final_range_vcsel_period_pclks = getVcselPulsePeriod(VcselPeriodFinalRange);

    timeouts->final_range_mclks = decodeTimeout(readReg16Bit(VL53L0X_FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI));

    if (enables->pre_range)
    {
        timeouts->final_range_mclks -= timeouts->pre_range_mclks;
    }

    timeouts->final_range_us = timeoutMclksToMicroseconds(timeouts->final_range_mclks, timeouts->final_range_vcsel_period_pclks);
}

uint16_t VL53L0X::decodeTimeout(uint16_t reg_val)
{
    /* format: "(LSByte * 2^MSByte) + 1" */
    return (uint16_t)((reg_val & 0x00FF) << (uint16_t)((reg_val & 0xFF00) >> 8)) + 1;
}

uint16_t VL53L0X::encodeTimeout(uint16_t timeout_mclks)
{
    /* format: "(LSByte * 2^MSByte) + 1" */

    uint32_t ls_byte = 0;
    uint16_t ms_byte = 0;

    if (timeout_mclks > 0)
    {
        ls_byte = timeout_mclks - 1;

        while ((ls_byte & 0xFFFFFF00) > 0)
        {
            ls_byte >>= 1;
            ms_byte++;
        }

        return (ms_byte << 8) | (ls_byte & 0xFF);
    }
    else
    {
        return 0;
    }
}

uint32_t VL53L0X::timeoutMclksToMicroseconds(uint16_t timeout_period_mclks, uint8_t vcsel_period_pclks)
{
    uint32_t macro_period_ns = calcMacroPeriod(vcsel_period_pclks);

    return ((timeout_period_mclks * macro_period_ns) + (macro_period_ns / 2)) / 1000;
}

uint32_t VL53L0X::timeoutMicrosecondsToMclks(uint32_t timeout_period_us, uint8_t vcsel_period_pclks)
{
    uint32_t macro_period_ns = calcMacroPeriod(vcsel_period_pclks);

    return (((timeout_period_us * 1000) + (macro_period_ns / 2)) / macro_period_ns);
}

bool VL53L0X::performSingleRefCalibration(uint8_t vhv_init_byte)
{
    writeReg(VL53L0X_SYSRANGE_START, 0x01 | vhv_init_byte);

    startTimeout();
    while ((readReg(VL53L0X_RESULT_INTERRUPT_STATUS) & 0x07) == 0)
    {
        if (checkTimeoutExpired())
        {
            return false;
        }
    }

    writeReg(VL53L0X_SYSTEM_INTERRUPT_CLEAR, 0x01);

    writeReg(VL53L0X_SYSRANGE_START, 0x00);

    return true;
}
