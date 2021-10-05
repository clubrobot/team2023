BOARD = esp32
CHIP = esp32

#Arduino file
SKETCH = main.ino
PART_FILE=$(ESP_ROOT)/tools/partitions/default.csv
BOARD_UUID = Actionneur
COMMON = ../../common
#Setup all libs used !
LIBS = 	$(ESP_LIBS)/EEPROM \
		$(COMMON)/AX12 \
		instructions.cpp \
		$(COMMON)/SerialTalks \
		$(COMMON)/CRC16 \
		$(COMMON)/Servo \


CPPFLAGS = -fexceptions
CPPFLAGS += -DCONFIG_CXX_EXCEPTIONS=1
CPPFLAGS += -DSERIALTALKS_MAX_OPCODE=0x30
CPPFLAGS += -DVL53L0X_LOG
CPPFLAGS += -DUSE_I2C_2V8
# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ../..
CPP_EXTRA += -fexceptions
include $(MODULEMK_DIR)/Module.mk

