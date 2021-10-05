# Board properties
BOARD = esp32
CHIP = esp32

#Arduino file
SKETCH = SerialTopics.ino

BOARD_UUID = SerialTopics
COMMON = ../common

#Setup all libs used !
LIBS =  $(ESP_LIBS)/EEPROM \
		instructions.cpp \
		topics.cpp \
		$(COMMON)/SerialTalks \
		$(COMMON)/CRC16 \
		$(COMMON)/SerialTopics
# Define
CPPFLAGS += -DSERIALTALKS_MAX_OPCODE=0x30


# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk