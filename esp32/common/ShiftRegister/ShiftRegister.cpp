#include "ShiftRegister.h"
#include <Arduino.h>

//global instace

void shiftOut(uint8_t dataPin, uint8_t clockPin, uint8_t bitOrder, byte val)
{
    int i;

    for (i = 0; i < 8; i++)
    {
        if (bitOrder == LSBFIRST)
        {
            digitalWrite(dataPin, !!(val & (1 << i)));
            delayMicroseconds(45);
        }
        else
        {
            digitalWrite(dataPin, !!(val & (1 << (7 - i))));
            delayMicroseconds(45);
        }

        digitalWrite(clockPin, HIGH);
        delayMicroseconds(45);
        digitalWrite(clockPin, LOW);
        delayMicroseconds(45);
    }
}

//ShiftRegister shift;

void ShiftRegister::attach(uint8_t latchpin, uint8_t clockpin, uint8_t datapin)
{
    m_LATCH = latchpin;
    m_CLOCK = clockpin;
    m_DATA = datapin;

    pinMode(m_LATCH, OUTPUT);
    pinMode(m_CLOCK, OUTPUT);
    pinMode(m_DATA, OUTPUT);

    m_register = 0;
}

void ShiftRegister::SetHigh(int pos)
{
    if (pos < m_size && pos >= 0)
    {
        m_register |= (1 << pos);
        shift();
    }
}

void ShiftRegister::SetLow(int pos)
{
    if (pos < m_size && pos >= 0)
    {
        m_register &= ~(1 << pos);
        shift();
    }
}

void ShiftRegister::shift()
{
    digitalWrite(m_LATCH, LOW);
    for (int i = m_size; i != 0; i -= SHIFT_REGISTER_1_BYTES)
    {
        shiftOut(m_DATA, m_CLOCK, MSBFIRST, (m_register >> (i - SHIFT_REGISTER_1_BYTES) & 0xFF));
    }
    digitalWrite(m_LATCH, HIGH);
}

void ShiftRegister::write(int pos, int state)
{
    if (state == 1)
        this->SetHigh(pos);
    else
        this->SetLow(pos);
}