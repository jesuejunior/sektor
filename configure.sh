#!/bin/bash
ip=$1

rsync -rav pi@$ip:~/code/sektor /sektor

conn="ssh pi@$ip"

# copy files to configure ports

# ....

${conn} 'sudo apt-get update'

${conn} 'sudo apt-get install --yes python3-pip pipenv build-essentials'

${conn} 'sudo cd /code && sudo pipenv install'


# Configuring port boudrate and starting gpsddeamon
${conn} 'stty -F /dev/ttyS0 9600 && sudo gpsd /dev/ttyS0 -F /var/run/gpsd.socket'


