#ifndef __SHIFTREGISTER_H__
#define __SHIFTREGISTER_H__

#include <Arduino.h>

#define SHIFT_REGISTER_1_BYTES (8)
#define SHIFT_REGISTER_2_BYTES (16)
#define SHIFT_REGISTER_3_BYTES (24)
#define SHIFT_REGISTER_4_BYTES (32)

class ShiftRegister
{
public:
    ShiftRegister() : m_size(SHIFT_REGISTER_1_BYTES) {}
    ShiftRegister(int size) : m_size(size) {}

    void attach(uint8_t latchpin, uint8_t clockpin, uint8_t datapin);
    void SetHigh(int pos);
    void SetLow(int pos);
    void write(int pos, int state);

    //protected:
    void shift();

    int m_size;

    uint8_t m_LATCH;
    uint8_t m_CLOCK;
    uint8_t m_DATA;

    volatile uint32_t m_register;
};
//extern ShiftRegister shift;
#endif // __SHIFTREGISTER_H__