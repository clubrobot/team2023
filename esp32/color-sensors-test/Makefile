BOARD = esp32
CHIP = esp32

PART_FILE=$(ESP_ROOT)/tools/partitions/default.csv

#Arduino file
SKETCH = color-sensors-test.ino

BOARD_UUID = ColorSensors
COMMON = ../common
#Setup all libs used !
LIBS =  $(ESP_LIBS)/EEPROM \
        $(ESP_LIBS)/Wire \
        $(COMMON)/SerialTalks \
        $(COMMON)/CRC16 \
        $(COMMON)/TCA9548A \
        $(COMMON)/TCS34725 \
        $(COMMON)/ColorSensors \
				instructions.cpp
# Define
CPPFLAGS += -DSERIALTALKS_MAX_OPCODE=0x30

# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk
