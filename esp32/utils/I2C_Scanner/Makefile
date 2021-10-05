BOARD = esp32
CHIP = esp32

#Arduino file
SKETCH = main.ino

BOARD_UUID = VL53L0X
COMMON = ../../common
#Setup all libs used !
LIBS = 	$(ESP_LIBS)/EEPROM \
		$(ESP_LIBS)/WIRE \


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

