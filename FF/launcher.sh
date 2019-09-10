#!/bin/sh
#launcher.sh

cd /
cd home/pi/FF2/
sudo python3 pirRUN.py &
sudo python3 routes.py &
sudo python3 twil.py &
sudo python3 dropb.py &
sudo python3 csvout.py &
sudo python3 wake_up.py
cd /
cd home/pi/
./ngrok tcp 22
cd /
