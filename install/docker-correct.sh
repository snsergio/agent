#!/bin/bash
clear
set -eo pipefail
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi
cd /opt/eyeflow/monitor/
if [ ! -f /opt/eyeflow/monitor/metric-collector-v5.py ]; then
    echo "There is no metric-collector-v5.py file in this folder, exiting..."
    exit
else
    rm metric-collector-v5.py
    wget https://raw.githubusercontent.com/snsergio/agent/main/metric-collector/metric-collector-v5.py
fi
cd lib
if [ ! -f /opt/eyeflow/monitor/lib/metricexporter.py ]; then
    echo "There is no metricexporter.py file in this folder, exiting..."
    exit
else
    rm metricexporter.py
    wget https://raw.githubusercontent.com/snsergio/agent/main/metric-collector/lib/metricexporter.py
fi
cd ..
systemctl restart metric-collector.service
cd $HOME
if [ ! -f /$HOME/docker-correct.sh ]; then
    echo "Please remove the docker correct script"
else
    rm -f /$HOME/docker-correct.sh
fi
systemctl status metric-collector.service
echo "DONE!"
