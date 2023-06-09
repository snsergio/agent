#!/bin/bash
# How to run: curl https://raw.githubusercontent.com/snsergio/agent/main/run_edge_install.sh | bash
wget https://raw.githubusercontent.com/snsergio/agent/main/install-edge.sh
sudo mv ./install-monitor.sh /opt/eyeflow/install/install-monitor.sh
chmod a+x /opt/eyeflow/install/install-monitor.sh
sudo source /opt/eyeflow/install/install-monitor.sh
echo "End of installation"
