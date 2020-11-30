# PaperoidPi
A thermal instant-camera based on Raspberry Pi and Paperang.

## Installation
The installation script will update your Pi and install all the dependencies:
```
chmod u+x install.sh
sudo ./install.sh
```
Be sure to have your camera interface enabled:
```
sudo raspi-config
```

## Config and run
Edit the `start.py` script to match your hardware configuration, then just:
```
sudo python3 start.py
```

## Run at boot
To run your Paperoid at boot, add the following line to `/etc/rc.local`:
```
sudo python3 /home/pi/PaperoidPi/start.py &
```

## To do
- Add a web interface to change camera settings
- Improve logging
