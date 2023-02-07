#ifndef __PIN_H__
#define __PIN_H__

#include <Arduino.h>

// Interrupt Pins

#define INTERRUPT_VL53L0X_1 18
#define INTERRUPT_VL53L0X_2 21
#define INTERRUPT_VL53L0X_3 3
#define INTERRUPT_VL53L0X_4 22
#define INTERRUPT_VL53L0X_5 27
#define INTERRUPT_VL53L0X_6 25
#define INTERRUPT_VL53L0X_7 32
#define INTERRUPT_VL53L0X_8 34

#define INTERRUPT_VL6180X_1 34
#define INTERRUPT_VL6180X_2 32
#define INTERRUPT_VL6180X_3 25
#define INTERRUPT_VL6180X_4 27
#define INTERRUPT_VL6180X_5 12
#define INTERRUPT_VL6180X_6 15
#define INTERRUPT_VL6180X_7 4
#define INTERRUPT_VL6180X_8 17

// I2C pins

#define SENSORS_SDA 2
#define SENSORS_SCL 4

// Shift register pin

#define SHIFT_REG_DATA 23
#define SHIFT_REG_CLOCK 18
#define SHIFT_REG_LATCH 19

#endif // __PIN_H__
