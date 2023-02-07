BOARD = esp32
CHIP = esp32

#Arduino file
SKETCH = main.ino

BOARD_UUID = VL53L0X
COMMON = ../../common
#Setup all libs used !
LIBS = 	$(ESP_LIBS)/EEPROM \
		$(ESP_LIBS)/WIRE 

LIBS_with_i=$(addprefix  -I, $(LIBS))


CPP_EXTRA = -fexceptions
CPP_EXTRA += -DCONFIG_CXX_EXCEPTIONS=1
CPP_EXTRA += -DSERIALTALKS_MAX_OPCODE=0x30
CPP_EXTRA += -DVL53L0X_LOG
CPP_EXTRA += -DUSE_I2C_2V8

# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ../../makefilesEsp
CPP_EXTRA += -fexceptions  $(LIBS_with_i)
include $(MODULEMK_DIR)/Module.mk

