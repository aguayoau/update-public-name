#!/bin/bash

############################################
#     
#     Please read the full instructions in Github
#     https://github.com/aguayoau/calendar_system/wiki
#
#########################################


source configuration


apt-get update
apt-get install python3 python3-pip


cat << _EOF_ > /etc/systemd/system/$SERVICE.service
[Unit]
Description=<application description>
After=syslog.target network.target

[Service]
Type=simple
User=root
PAMName=login
PIDFile=/run/<application>.pid
ExecStart=/usr/bin/python3 -u /opt/<application>
WorkingDirectory=/run/

[Install]
WantedBy=multi-user.target
_EOF_

sed -i "s/<application>/$APPLICATION/g" /etc/systemd/system/$SERVICE.service
sed -i "s/<application description>/$APPLICATIONDESC/g" /etc/systemd/system/$SERVICE.service
cp  -R ../opt/$APPLICATION /opt/$APPLICATION
chmod 755 /opt/$APPLICATION/*.py


systemctl daemon-reload
systemctl enable $SERVICE.service
if [ -f /opt/$APPLICATION/cron.py ] 
then
    systemctl start $SERVICE.service
fi

