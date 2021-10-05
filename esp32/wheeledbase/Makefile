BOARD = esp32
CHIP = esp32

#Arduino file
SKETCH = wheeledbase.ino

BOARD_UUID = wheeledbase
COMMON = ../common
#Setup all libs used !
LIBS =  $(ESP_LIBS)/EEPROM \
		$(COMMON)/SerialTalks \
		$(COMMON)/CRC16 \
		$(COMMON)/mathutils\
		$(COMMON)/DCMotor \
		$(COMMON)/Codewheel \
		$(COMMON)/PeriodicProcess \
		$(COMMON)/Odometry \
		$(COMMON)/PID \
		$(COMMON)/DifferentialController \
		$(COMMON)/VelocityController \
		$(COMMON)/PositionController \
		$(COMMON)/PurePursuit \
		$(COMMON)/TurnOnTheSpot \
		$(COMMON)/mathutils \
		$(COMMON)/TaskManager \
		instructions.cpp
# Define
CPPFLAGS += -DSERIALTALKS_MAX_OPCODE=0x30
CPPFLAGS += -DPUREPURSUIT_MAX_WAYPOINTS=32


# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk

