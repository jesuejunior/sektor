#!/bin/bash

DIRECTORY="/var/run/sektor"
start() {
  
  stty -F /dev/ttyS0 9600 
  gpsd /dev/ttyS0 -F /var/run/gpsd.socket
  
  if [ ! -d "$DIRECTORY" ]; then
    sudo mkdir -p $DIRECTORY
  fi
  echo "Starting sektor service"
  cd /opt/sektor; python3 sektor/main.py
}

stop() {
  killall main.py
}

case $1 in
  start|stop) "$1" ;;
esac
