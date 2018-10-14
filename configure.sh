#!/bin/bash
ip=$1

conn="ssh pi@$ip"

${conn} 'sudo apt-get update && sudo apt-get install --yes python3-pip build-essential rsync && sudo pip3 install pipenv'

rsync -rav ../sektor pi@$ip:~/code/sektor

${conn} 'cd /code/sektor; sudo pipenv --python /usr/bin/python3 install && sudo chmod +x /code/sektor/sektor/main.py'

# Configuring port boudrate and starting gpsddeamon
#${conn} 'stty -F /dev/ttyS0 9600 && sudo gpsd /dev/ttyS0 -F /var/run/gpsd.socket'


${conn} 'sudo cp /code/sektor/files/sektor.service /lib/systemd/system/sektor.service && sudo systemctl daemon-reload && sudo systemctl enable sektor.service'


