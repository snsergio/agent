#!/bin/bash
clear
set -eo pipefail
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi
curl https://raw.githubusercontent.com/snsergio/agent/main/install-edge.sh
chmod +x install-edge.sh
sudo source /opt/eyeflow/install/install-monitor.sh
echo "End of installation"
