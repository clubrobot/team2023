# Club Robot INSA Rennes 2022

> Software solution of the 2021/2022 Robotics Club of INSA Rennes

## How to clone the repository ?

1. Create your working directory as follow :
   `mkdir WORKING_DIRECTORY`

2. Then go into your new WOTKING_DIRECTORY :
   `cd WORKING_DIRECTORY`

3. Now, you can clone the repository :

   - https method : `git clone https://github.com/clubrobot/team-2022.git`
   - ssh method : `git clone git@github.com:clubrobot/team-2022.git`

4. Well Done ! The code is now on your computer.

## How to setup the project ?

> The next step is to configure the project and download all the required tools and libraries.

1. Just run the bash setup script :
   `./setup.sh`

2. After the setup script, you need to restart you computer.


## On Windows and using WSL

> Not very easy but can be done:
1. Make sure arduino.mk is properly configured and setup.sh has ran by doing `make` in a arduino code folder
   You may need to update some paths var in the .profile file at your home:
>Setup.sh does not work very well at setting paths in wsl >> todo
```
export ARDUINO_DIR=/opt/arduino-1.6.12
export ESP_ROOT=/hardware/espressif/esp32
export ARDMK_DIR=/usr/share/arduino
export PATH=/team2023/raspberrypi:$PATH
```
2. If compiling working you can now upload but you still need a program:
   Install the [latest release of usbipd-win](https://github.com/dorssel/usbipd-win/releases)
>This will make a localhost bridge between windows and wsl
   In WSL install some packages:
```
sudo apt install linux-tools-5.4.0-77-generic hwdata
sudo update-alternatives --install /usr/local/bin/usbip usbip /usr/lib/linux-tools/5.4.0-77-generic/usbip 20
```
3. Attach a device:
do `usbipd wsl list` in an **elevated** windows cmd then slect the bus ID corresponding to your arduino device and run
`usbipd wsl attach --busid <busid>`
Now in WSL, you can list your USB device by doing `lsusb`
4. Don't forget to detach tour arduino
>to clean your computer don't dorget to run `usbipd wsl detach --busid <busid>` in an **elevated** windows cmd