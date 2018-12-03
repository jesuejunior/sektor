#!/bin/bash
ip=$1

conn="ssh pi@$ip"
DIR="/opt/sektor"

echo "Installing and configure packages and directories"
${conn} "sudo apt-get update \
    && sudo apt-get install --yes python3-pip build-essential rsync \
    && sudo pip3 install pipenv \
    && sudo mkdir -p $DIR \
    && sudo chmod -R 775 $DIR \
    && sudo chown pi -R $DIR"

echo "Starting project sync"
rsync -rav --delete --exclude ".git"  ../sektor pi@$ip:/opt/
echo "Sync is done"

echo "Preparing project, installing dependencies using pipenv "
${conn} "cd /opt/sektor; sudo pipenv --python /usr/bin/python3 install && sudo chmod +x /opt/sektor/sektor/main.py"

echo "Adding sektor as a service to start on boot"
${conn} "sudo cp -f /opt/sektor/files/sektor.service /lib/systemd/system/sektor.service && sudo systemctl daemon-reload && sudo systemctl enable sektor.service"

