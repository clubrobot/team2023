# Board properties
BOARD = esp32doit-devkit-v1
CHIP = esp32

#Arduino file
SKETCH = sensors.ino

BOARD_UUID = sensors
COMMON = ../common
BUILD_DIR =../build
#EXPAND_LIBS=1
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
		$(COMMON) \
		$(COMMON)/TaskManager  \
		$(COMMON)/serialutils.cpp
#$(COMMON)/thread_tools.cpp 

LIBS_with_i=$(addprefix  -I, $(LIBS))

# Define
CPP_EXTRA += -DSERIALTALKS_MAX_OPCODE=0x18 $(LIBS_with_i)

CPP_EXTRA += -DBOARD_UUID=\"sensors\"
CPP_EXTRA += -DLOG_LEVEL=6

# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ../makefilesEsp
include $(MODULEMK_DIR)/Module.mk