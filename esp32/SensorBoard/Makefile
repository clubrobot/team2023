# Board properties
BOARD = esp32
CHIP = esp32

#Arduino file
SKETCH = SensorBoard.ino

BOARD_UUID = SensorBoard
COMMON = ../common

#Setup all libs used !
LIBS =  $(ESP_LIBS)/EEPROM \
		$(ESP_LIBS)/Wire \
		instructions.cpp \
		topics.cpp \
		$(COMMON)/SerialTalks \
		$(COMMON)/CRC16 \
		$(COMMON)/SerialTopics \
		$(COMMON)/ShiftRegister \
		$(COMMON)/VL6180X \
		$(COMMON)/VL53L0X \
		$(COMMON)/TaskManager
# Define
CPPFLAGS += -DSERIALTALKS_MAX_OPCODE=0x30


# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk