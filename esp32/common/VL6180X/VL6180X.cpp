#include "VL6180X.h"
#include "VL6180X_tuning.h"

// Defines /////////////////////////////////////////////////////////////////////

// RANGE_SCALER values for 1x, 2x, 3x scaling - see STSW-IMG003 core/src/vl6180x_api.c (ScalerLookUP[])
static uint16_t const ScalerValues[] = {0, 253, 127, 84};

// Constructors ////////////////////////////////////////////////////////////////

VL6180X::VL6180X(uint8_t i2c_addr, uint8_t shutdown_pin, ShiftRegister *shift_reg, TwoWire *i2c)
    : _i2c_addr(i2c_addr), _shutdown_pin(shutdown_pin), _shift_reg(shift_reg), _i2c(i2c)
{
    _scaling = 0;
    _ptp_offset = 0;
    _io_timeout = 0;
    _did_timeout = false;
    _init_state = false;
}

// Public Methods //////////////////////////////////////////////////////////////

void VL6180X::setAddress(uint8_t new_addr)
{
    _i2c->beginTransmission(VL6180X_I2C_ADDR);
    _i2c->write((VL6180X_I2C_SLAVE__DEVICE_ADDRESS >> 8) & 0xff); // reg high byte
    _i2c->write(VL6180X_I2C_SLAVE__DEVICE_ADDRESS & 0xff);        // reg low byte
    _i2c->write(new_addr & 0x7F);
    _last_status = _i2c->endTransmission();
}

void VL6180X::load_tunning_settings()
{
    for (unsigned int i = 0; i < (sizeof(VL6180X_tuning_table) / sizeof(VL6180X_tuning_t)); i++)
    {
        writeReg(VL6180X_tuning_table[i].reg, VL6180X_tuning_table[i].value);
    }
}

void VL6180X::shutdown()
{
    /* always shutdown the sensor at the beggining */
    if (_shutdown_pin != NULL)
    {
        if (_shift_reg != NULL)
        {
            _shift_reg->SetLow(_shutdown_pin);
        }
        else
        {
            pinMode(_shutdown_pin, OUTPUT);
            digitalWrite(_shutdown_pin, LOW);
        }
    }
}

// Initialize sensor with settings from ST application note AN4545, section 9 -
// "Mandatory : private registers"
bool VL6180X::begin()
{
    /* enable the sensor */
    if (_shutdown_pin != NULL)
    {
        if (_shift_reg != NULL)
        {
            _shift_reg->SetHigh(_shutdown_pin);
            delay(2);
        }
        else
        {
            digitalWrite(_shutdown_pin, HIGH);
            delay(2);
        }
    }
    setAddress(_i2c_addr);
    // Store part-to-part range offset so it can be adjusted if scaling is changed
    _ptp_offset = readReg(VL6180X_SYSRANGE__PART_TO_PART_RANGE_OFFSET);

    if (readReg(VL6180X_SYSTEM__FRESH_OUT_OF_RESET) == 1)
    {
        _scaling = 1;

        load_tunning_settings();

        writeReg(VL6180X_SYSTEM__FRESH_OUT_OF_RESET, 0);
    }
    else
    {
        // Sensor has already been initialized, so try to get scaling settings by
        // reading registers.

        uint16_t s = readReg16Bit(VL6180X_RANGE_SCALER);

        if (s == ScalerValues[3])
        {
            _scaling = 3;
        }
        else if (s == ScalerValues[2])
        {
            _scaling = 2;
        }
        else
        {
            _scaling = 1;
        }

        // Adjust the part-to-part range offset value read earlier to account for
        // existing scaling. If the sensor was already in 2x or 3x scaling mode,
        // precision will be lost calculating the original (1x) offset, but this can
        // be resolved by resetting the sensor and Arduino again.
        _ptp_offset *= _scaling;
    }

    _init_state = true;

    return true;
}

// Configure some settings for the sensor's default behavior from AN4545 -
// "Recommended : Public registers" and "Optional: Public registers"
//
// Note that this function does not set up GPIO1 as an interrupt output as
// suggested, though you can do so by calling:
// writeReg(SYSTEM__MODE_GPIO1, 0x10);
void VL6180X::configureDefault(void)
{
    // "Recommended : Public registers"

    // readout__averaging_sample_period = 48 (0x30)
    writeReg(VL6180X_READOUT__AVERAGING_SAMPLE_PERIOD, 0xF0);

    // sysals__analogue_gain_light = 6 (ALS gain = 1 nominal, actually 1.01 according to Table 14 in datasheet)
    writeReg(VL6180X_SYSALS__ANALOGUE_GAIN, 0x46);

    // sysrange__vhv_repeat_rate = 255 (auto Very High Voltage temperature recalibration after every 255 range measurements)
    writeReg(VL6180X_SYSRANGE__VHV_REPEAT_RATE, 0xFF);

    // sysals__integration_period = 99 (100 ms)
    // AN4545 incorrectly recommends writing to register 0x040; 0x63 should go in the lower byte, which is register 0x041.
    writeReg16Bit(VL6180X_SYSALS__INTEGRATION_PERIOD, 0x0063);

    // sysrange__vhv_recalibrate = 1 (manually trigger a VHV recalibration)
    writeReg(VL6180X_SYSRANGE__VHV_RECALIBRATE, 0x01);

    // "Optional: Public registers"

    // sysrange__intermeasurement_period = 9 (100 ms)
    writeReg(VL6180X_SYSRANGE__INTERMEASUREMENT_PERIOD, 0x09);

    // sysals__intermeasurement_period = 49 (500 ms)
    writeReg(VL6180X_SYSALS__INTERMEASUREMENT_PERIOD, 0x31);

    // als_int_mode = 4 (ALS new sample ready interrupt); range_int_mode = 4 (range new sample ready interrupt)
    writeReg(VL6180X_SYSTEM__INTERRUPT_CONFIG_GPIO, 0x24);

    // Reset other settings to power-on defaults

    // sysrange__max_convergence_time = 49 (49 ms)
    writeReg(VL6180X_SYSRANGE__MAX_CONVERGENCE_TIME, 0x31);

    // disable interleaved mode
    writeReg(VL6180X_INTERLEAVED_MODE__ENABLE, 0);

    // reset range scaling factor to 1x
    setScaling(1);
}

// Writes an 8-bit register
void VL6180X::writeReg(uint16_t reg, uint8_t value)
{
    _i2c->beginTransmission(_i2c_addr);
    _i2c->write((reg >> 8) & 0xff); // reg high byte
    _i2c->write(reg & 0xff);        // reg low byte
    _i2c->write(value);
    _last_status = _i2c->endTransmission();
}

// Writes a 16-bit register
void VL6180X::writeReg16Bit(uint16_t reg, uint16_t value)
{
    _i2c->beginTransmission(_i2c_addr);
    _i2c->write((reg >> 8) & 0xff);   // reg high byte
    _i2c->write(reg & 0xff);          // reg low byte
    _i2c->write((value >> 8) & 0xff); // value high byte
    _i2c->write(value & 0xff);        // value low byte
    _last_status = _i2c->endTransmission();
}

// Writes a 32-bit register
void VL6180X::writeReg32Bit(uint16_t reg, uint32_t value)
{
    _i2c->beginTransmission(_i2c_addr);
    _i2c->write((reg >> 8) & 0xff);    // reg high byte
    _i2c->write(reg & 0xff);           // reg low byte
    _i2c->write((value >> 24) & 0xff); // value highest byte
    _i2c->write((value >> 16) & 0xff);
    _i2c->write((value >> 8) & 0xff);
    _i2c->write(value & 0xff); // value lowest byte
    _last_status = _i2c->endTransmission();
}

// Reads an 8-bit register
uint8_t VL6180X::readReg(uint16_t reg)
{
    uint8_t value;

    _i2c->beginTransmission(_i2c_addr);
    _i2c->write((reg >> 8) & 0xff); // reg high byte
    _i2c->write(reg & 0xff);        // reg low byte
    _last_status = _i2c->endTransmission();

    _i2c->requestFrom(_i2c_addr, (uint8_t)1);
    value = _i2c->read();
    _i2c->endTransmission();

    return value;
}

// Reads a 16-bit register
uint16_t VL6180X::readReg16Bit(uint16_t reg)
{
    uint16_t value;

    _i2c->beginTransmission(_i2c_addr);
    _i2c->write((reg >> 8) & 0xff); // reg high byte
    _i2c->write(reg & 0xff);        // reg low byte
    _last_status = _i2c->endTransmission();

    _i2c->requestFrom(_i2c_addr, (uint8_t)2);
    value = (uint16_t)_i2c->read() << 8; // value high byte
    value |= _i2c->read();               // value low byte
    _i2c->endTransmission();

    return value;
}

// Reads a 32-bit register
uint32_t VL6180X::readReg32Bit(uint16_t reg)
{
    uint32_t value;

    _i2c->beginTransmission(_i2c_addr);
    _i2c->write((reg >> 8) & 0xff); // reg high byte
    _i2c->write(reg & 0xff);        // reg low byte
    _last_status = _i2c->endTransmission();

    _i2c->requestFrom(_i2c_addr, (uint8_t)4);
    value = (uint32_t)_i2c->read() << 24; // value highest byte
    value |= (uint32_t)_i2c->read() << 16;
    value |= (uint16_t)_i2c->read() << 8;
    value |= _i2c->read(); // value lowest byte
    _i2c->endTransmission();

    return value;
}

// Set range scaling factor. The sensor uses 1x scaling by default, giving range
// measurements in units of mm. Increasing the scaling to 2x or 3x makes it give
// raw values in units of 2 mm or 3 mm instead. In other words, a bigger scaling
// factor increases the sensor's potential maximum range but reduces its
// resolution.

// Implemented using ST's VL6180X API as a reference (STSW-IMG003); see
// VL6180x_UpscaleSetScaling() in vl6180x_api.c.
void VL6180X::setScaling(uint8_t new_scaling)
{
    uint8_t const DefaultCrosstalkValidHeight = 20; // default value of SYSRANGE__CROSSTALK_VALID_HEIGHT

    // do nothing if scaling value is invalid
    if (new_scaling < 1 || new_scaling > 3)
    {
        return;
    }

    _scaling = new_scaling;
    writeReg16Bit(VL6180X_RANGE_SCALER, ScalerValues[_scaling]);

    // apply scaling on part-to-part offset
    writeReg(VL6180X_SYSRANGE__PART_TO_PART_RANGE_OFFSET, _ptp_offset / _scaling);

    // apply scaling on CrossTalkValidHeight
    writeReg(VL6180X_SYSRANGE__CROSSTALK_VALID_HEIGHT, DefaultCrosstalkValidHeight / _scaling);

    // This function does not apply scaling to RANGE_IGNORE_VALID_HEIGHT.

    // enable early convergence estimate only at 1x scaling
    uint8_t rce = readReg(VL6180X_SYSRANGE__RANGE_CHECK_ENABLES);
    writeReg(VL6180X_SYSRANGE__RANGE_CHECK_ENABLES, (rce & 0xFE) | (_scaling == 1));
}

// Performs a single-shot ranging measurement
uint8_t VL6180X::readRangeSingle()
{
    writeReg(VL6180X_SYSRANGE__START, 0x01);
    return readRangeContinuous();
}

// Performs a single-shot ambient light measurement
uint16_t VL6180X::readAmbientSingle()
{
    writeReg(VL6180X_SYSALS__START, 0x01);
    return readAmbientContinuous();
}

// Starts continuous ranging measurements with the given period in ms
// (10 ms resolution; defaults to 100 ms if not specified).
//
// The period must be greater than the time it takes to perform a
// measurement. See section 2.4.4 ("Continuous mode limits") in the datasheet
// for details.
void VL6180X::startRangeContinuous(uint16_t period)
{
    int16_t period_reg = (int16_t)(period / 10) - 1;
    period_reg = constrain(period_reg, 0, 254);

    writeReg(VL6180X_SYSRANGE__INTERMEASUREMENT_PERIOD, period_reg);
    writeReg(VL6180X_SYSRANGE__START, 0x03);
}

// Starts continuous ambient light measurements with the given period in ms
// (10 ms resolution; defaults to 500 ms if not specified).
//
// The period must be greater than the time it takes to perform a
// measurement. See section 2.4.4 ("Continuous mode limits") in the datasheet
// for details.
void VL6180X::startAmbientContinuous(uint16_t period)
{
    int16_t period_reg = (int16_t)(period / 10) - 1;
    period_reg = constrain(period_reg, 0, 254);

    writeReg(VL6180X_SYSALS__INTERMEASUREMENT_PERIOD, period_reg);
    writeReg(VL6180X_SYSALS__START, 0x03);
}

// Starts continuous interleaved measurements with the given period in ms
// (10 ms resolution; defaults to 500 ms if not specified). In this mode, each
// ambient light measurement is immediately followed by a range measurement.
//
// The datasheet recommends using this mode instead of running "range and ALS
// continuous modes simultaneously (i.e. asynchronously)".
//
// The period must be greater than the time it takes to perform both
// measurements. See section 2.4.4 ("Continuous mode limits") in the datasheet
// for details.
void VL6180X::startInterleavedContinuous(uint16_t period)
{
    int16_t period_reg = (int16_t)(period / 10) - 1;
    period_reg = constrain(period_reg, 0, 254);

    writeReg(VL6180X_INTERLEAVED_MODE__ENABLE, 1);
    writeReg(VL6180X_SYSALS__INTERMEASUREMENT_PERIOD, period_reg);
    writeReg(VL6180X_SYSALS__START, 0x03);
}

// Stops continuous mode. This will actually start a single measurement of range
// and/or ambient light if continuous mode is not active, so it's a good idea to
// wait a few hundred ms after calling this function to let that complete
// before starting continuous mode again or taking a reading.
void VL6180X::stopContinuous()
{

    writeReg(VL6180X_SYSRANGE__START, 0x01);
    writeReg(VL6180X_SYSALS__START, 0x01);

    writeReg(VL6180X_INTERLEAVED_MODE__ENABLE, 0);
}

// Returns a range reading when continuous mode is activated
// (readRangeSingle() also calls this function after starting a single-shot
// range measurement)
uint8_t VL6180X::readRangeContinuous()
{
    uint16_t millis_start = millis();
    while ((readReg(VL6180X_RESULT__INTERRUPT_STATUS_GPIO) & 0x04) == 0)
    {
        if (_io_timeout > 0 && ((uint16_t)millis() - millis_start) > _io_timeout)
        {
            _did_timeout = true;
            return _previousRange;
        }
    }
    uint8_t range = _previousRange;

    uint8_t errorCode = readReg(VL6180X_RESULT__RANGE_STATUS);
    if ((errorCode & 0xF0) != 0xB0)
    { //Check if SNR Error on result
        range = readReg(VL6180X_RESULT__RANGE_VAL);
        _previousRange = range;
    }
    writeReg(VL6180X_SYSTEM__INTERRUPT_CLEAR, 0x01);

    return range;
}

// Returns an ambient light reading when continuous mode is activated
// (readAmbientSingle() also calls this function after starting a single-shot
// ambient light measurement)
uint16_t VL6180X::readAmbientContinuous()
{
    uint16_t millis_start = millis();
    while ((readReg(VL6180X_RESULT__INTERRUPT_STATUS_GPIO) & 0x20) == 0)
    {
        if (_io_timeout > 0 && ((uint16_t)millis() - millis_start) > _io_timeout)
        {
            _did_timeout = true;
            return 0;
        }
    }

    uint16_t ambient = readReg16Bit(VL6180X_RESULT__ALS_VAL);
    writeReg(VL6180X_SYSTEM__INTERRUPT_CLEAR, 0x02);

    return ambient;
}

// Did a timeout occur in one of the read functions since the last call to
// timeoutOccurred()?
bool VL6180X::timeoutOccurred()
{
    bool tmp = _did_timeout;
    _did_timeout = false;
    return tmp;
}
