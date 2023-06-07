#!/bin/bash
# LOG file at /opt/eyeflow/install/monitor-install-<date time>.log
set -eo pipefail
mkdir -p /opt/eyeflow/install
touch /opt/eyeflow/install/monitor-install.log
echo "##### Installing Eyeflow Monitoring agent on EDGE server #####" | sudo tee -a /opt/eyeflow/install/monitor-install.log
date | sudo tee -a /opt/eyeflow/install/monitor-install.log
if [ "$EUID" -ne 0 ]
    then echo "Please run as root" | sudo tee -a /opt/eyeflow/install/monitor-install.log
    exit
fi
lspci | grep -i nvidia &> /dev/null
if [ ! $? == 0 ]
    then echo "No NVIDIA GPU found, ensure correct collector configuration" | sudo tee -a /opt/eyeflow/install/monitor-install.log
fi
lspci | grep -i nvidia | sudo tee -a /opt/eyeflow/install/monitor-install.log
if [ ! $(lsb_release -si) == "Ubuntu" ]
    then echo "OS distribution is not Ubuntu, exiting..." | sudo tee -a /opt/eyeflow/install/monitor-install.log
    exit
fi
lsb_release -si | sudo tee -a /opt/eyeflow/install/monitor-install.log
lsb_release -sr | sudo tee -a /opt/eyeflow/install/monitor-install.log
cp ./install-monitor.sh /opt/eyeflow/install/install-monitor.sh
echo "##### running installation script.." | sudo tee -a /opt/eyeflow/install/monitor-install.log
apt update | sudo tee -a /opt/eyeflow/install/monitor-install.log
apt -y upgrade | sudo tee -a /opt/eyeflow/install/monitor-install.log
echo "##### Installing initial packages" | sudo tee -a /opt/eyeflow/install/monitor-install.log
apt install -y curl lm-sensors sysstat iproute2 python3-requests
echo "##### Installing GIT:" | sudo tee -a /opt/eyeflow/install/monitor-install.log
apt install -y git acl
echo "##### Install PIP packages" | sudo tee -a /opt/eyeflow/install/monitor-install.log
/usr/bin/python3 -m pip install xmltodict==0.13.0 \
    prometheus_client==0.16.0 \
    requests==2.28.2 \
    PyYAML==6.0
mkdir -p /opt/eyeflow/monitor/lib
echo "##### Cloning Edge repo and setting rights" | sudo tee -a /opt/eyeflow/install/monitor-install.log
cd /opt/eyeflow/install
rm -rf /opt/eyeflow/install/agent
git clone https://github.com/snsergio/agent.git
chown -R eyeflow:users /opt/eyeflow/monitor
setfacl -dm u::rwx,g::rwx,o::rx /opt/eyeflow/monitor
chmod g+rwxs /opt/eyeflow/monitor
chmod 775 /opt/eyeflow/monitor
rsync -zvrh /opt/eyeflow/install/agent/* /opt/eyeflow/monitor
cd /opt/eyeflow/monitor
echo "##### Editing monitoring agent configuration file" | sudo tee -a /opt/eyeflow/install/monitor-install.log
echo "#################################################################################"
echo "# Edit Monitoring Agent configuration file to reflect Edge Station requirements #"
echo "#   Press <ENTER> to edit or <CTRL-C> to cancel Monitoring Agent instalation    #"
echo "#################################################################################"
read -s -n 1
nano /opt/eyeflow/monitor/collector-config.yaml
echo "##### Copying metric collector service to systemd" | sudo tee -a /opt/eyeflow/install/monitor-install.log
sudo cp /opt/eyeflow/monitor/metric-collector.service /etc/systemd/system/. 
echo "##### Starting collector agent" | sudo tee -a /opt/eyeflow/install/monitor-install.log
sudo systemctl enable metric-collector.service 
sudo systemctl start metric-collector.service 
sudo systemctl status metric-collector.service | sudo tee -a /opt/eyeflow/install/monitor-install.log
echo "##### Remove temporary files" | sudo tee -a /opt/eyeflow/install/monitor-install.log
rm -f /home/eyeflow/install-monitor.sh
echo "##### end of script" | sudo tee -a /opt/eyeflow/install/monitor-install.log
date | sudo tee -a /opt/eyeflow/install/monitor-install.log
mv /opt/eyeflow/install/monitor-install.log /opt/eyeflow/install/monitor-install-$(date +%F-%H:%M).log
echo "####################################################################"
echo "# LOG file at: /opt/eyeflow/install/monitor-install<date time>.log #"
echo "####################################################################"

