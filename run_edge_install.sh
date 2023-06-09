#!/bin/bash
# How to run: curl https://raw.githubusercontent.com/snsergio/agent/main/run_edge_install.sh | bash
wget https://raw.githubusercontent.com/snsergio/agent/main/install-edge.sh
sudo mv ./install-edge.sh /opt/eyeflow/install/install-edge.sh
chmod a+x /opt/eyeflow/install/install-edge.sh
sudo bash /opt/eyeflow/install/install-edge.sh
echo "End of installation"
rm -f install-edge.sh
