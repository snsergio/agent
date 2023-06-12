#!/bin/bash
# LOG file at /opt/eyeflow/install/monitor-install-<date time>.log
set -eo pipefail
mkdir -p /opt/eyeflow/install
if [ -f /opt/eyeflow/install/edge-install.log ]; then
    LOGFILE="/opt/eyeflow/install/edge-install.log"
else
    LOGFILE="/opt/eyeflow/install/monitor-install.log"
    touch /opt/eyeflow/install/monitor-install.log
fi
echo "##### Installing Eyeflow Monitoring agent on EDGE server #####" | sudo tee -a $LOGFILE
date | sudo tee -a $LOGFILE
if [ "$EUID" -ne 0 ]
    then echo "Please run as root" | sudo tee -a $LOGFILE
    exit
fi
lspci | grep -i nvidia &> /dev/null
if [ ! $? == 0 ]
    then echo "No NVIDIA GPU found, ensure correct collector configuration" | sudo tee -a $LOGFILE
fi
lspci | grep -i nvidia | sudo tee -a $LOGFILE
if [ ! $(lsb_release -si) == "Ubuntu" ]
    then echo "OS distribution is not Ubuntu, exiting..." | sudo tee -a $LOGFILE
    exit
fi
lsb_release -si | sudo tee -a $LOGFILE
lsb_release -sr | sudo tee -a $LOGFILE
if [[ ! $PWD = /opt/eyeflow/install ]]; then
    cp ./install-monitor.sh /opt/eyeflow/install/install-monitor.sh
fi
echo "##### running installation script.." | sudo tee -a $LOGFILE
apt update | sudo tee -a $LOGFILE
apt -y upgrade | sudo tee -a $LOGFILE
echo "##### Installing initial packages" | sudo tee -a $LOGFILE
apt install -y curl lm-sensors sysstat iproute2 python3-requests
echo "##### Installing GIT:" | sudo tee -a $LOGFILE
apt install -y git acl
echo "##### Install PIP packages" | sudo tee -a $LOGFILE
/usr/bin/python3 -m pip install xmltodict==0.13.0 \
    prometheus_client==0.16.0 \
    requests==2.28.2 \
    PyYAML==6.0
mkdir -p /opt/eyeflow/monitor/lib
echo "##### Cloning Edge repo and setting rights" | sudo tee -a $LOGFILE
cd /opt/eyeflow/install
rm -rf /opt/eyeflow/install/agent
git clone https://github.com/snsergio/agent.git
chown -R eyeflow:users /opt/eyeflow/monitor
setfacl -dm u::rwx,g::rwx,o::rx /opt/eyeflow/monitor
chmod g+rwxs /opt/eyeflow/monitor
chmod 775 /opt/eyeflow/monitor
rsync -zvrh /opt/eyeflow/install/agent/* /opt/eyeflow/monitor
cd /opt/eyeflow/monitor
echo "##### Editing monitoring agent configuration file" | sudo tee -a $LOGFILE
echo "#################################################################################"
echo "# Edit Monitoring Agent configuration file to reflect Edge Station requirements #"
echo "#   Press <ENTER> to edit or <CTRL-C> to cancel Monitoring Agent instalation    #"
echo "#################################################################################"
read -s -n 1
nano /opt/eyeflow/monitor/collector-config-v4.yaml
echo "##### Copying metric collector service to systemd" | sudo tee -a $LOGFILE
cp /opt/eyeflow/monitor/metric-collector.service /etc/systemd/system/. 
echo "##### Starting collector agent" | sudo tee -a $LOGFILE
systemctl enable metric-collector.service 
systemctl start metric-collector.service 
systemctl status metric-collector.service | sudo tee -a $LOGFILE
echo "##### Remove temporary files" | sudo tee -a $LOGFILE
rm -f /home/eyeflow/install-monitor.sh
rm -rf /opt/eyeflow/install/agent
echo "###########################################################" | sudo tee -a $LOGFILE
echo "#####   end of Metric Collector installation script   #####" | sudo tee -a $LOGFILE
echo "##### Finished at: $(date)" | sudo tee -a $LOGFILE
if [ ! -f /opt/eyeflow/install/edge-install.log ]; then
    mv $LOGFILE /opt/eyeflow/install/monitor-install-$(date +%F-%H:%M).log
    echo "####################################################################"
    echo "# LOG file at: /opt/eyeflow/install/monitor-install<date time>.log #"
    echo "####################################################################"
fi
