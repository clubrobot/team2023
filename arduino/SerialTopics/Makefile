# Board properties
BOARD_UUID = wheeledbase
BOARD_TAG  = nano
BOARD_SUB  = atmega328

# Sketch sources
COMMON = ../common
LOCAL_INO_SRCS = SerialTopics.ino
LOCAL_CPP_SRCS = \
	instructions.cpp \
	topics.cpp \
	$(COMMON)/SerialTalks.cpp \
	$(COMMON)/CRC16.cpp \
	$(COMMON)/SerialTopics.cpp 

# Define
CPPFLAGS += -DSERIALTALKS_MAX_OPCODE=0x30

# Sketch libraries
ARDUINO_LIBS = EEPROM

# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk
