#!/bin/bash
# LOG file at /opt/eyeflow/install/monitor-install-<date time>.log
# wget --no-cookies --no-cache https://raw.githubusercontent.com/snsergio/agent/main/install-monitor.sh
# chmod +x install-monitor.sh
# sudo ./install-monitor.sh
##### Install Monitor v5.10
set -eo pipefail
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi
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
gpu=$(/usr/bin/lspci | grep -i '.* vga .* nvidia .*')
if [[ -z $gpu ]]; then gpu="none"
shopt -s nocasematch
if [[ $gpu == *' nvidia '* ]]
    then echo "No NVIDIA GPU found, ensure correct collector configuration" | sudo tee -a $LOGFILE
fi
echo $gpu | sudo tee -a $LOGFILE
if [ ! $(lsb_release -si) == "Ubuntu" ]
    then echo "OS distribution is not Ubuntu, exiting..." | sudo tee -a $LOGFILE
    exit
fi
lsb_release -si | sudo tee -a $LOGFILE
lsb_release -sr | sudo tee -a $LOGFILE
if [[ ! $PWD = /opt/eyeflow/install ]]; then
    cp ./install-monitor.sh /opt/eyeflow/install/install-monitor.sh
fi
clear
echo "##### running installation script.." | sudo tee -a $LOGFILE
while true; do
    read -p "Do you want to UPDATE and UPGRADE OS? (y/n) " yn
    case $yn in 
        [yY] ) echo "##### updating and upgrading OS..." | sudo tee -a $LOGFILE;
            apt update | sudo tee -a $LOGFILE
            apt -y upgrade | sudo tee -a $LOGFILE
            break;;
        [nN] ) echo "##### continuing without update and upgrade..." | sudo tee -a $LOGFILE;
            break;;
        * ) echo invalid response;;
    esac
done
echo "##### resuming installation script.." | sudo tee -a $LOGFILE
echo "##### Installing initial packages" | sudo tee -a $LOGFILE
apt install -y curl lm-sensors sysstat ntpstat netcat iproute2 python3-requests python3-pip unzip
echo "##### Installing GIT:" | sudo tee -a $LOGFILE
apt install -y git acl
echo "##### Install PIP packages" | sudo tee -a $LOGFILE
/usr/bin/python3 -m pip install xmltodict==0.13.0 \
    prometheus_client==0.16.0 \
    requests==2.28.2 \
    PyYAML
if [ $(uname -i) == "aarch64" ]; then
    echo "##### Installing ARM jetson-stats" | sudo tee -a $LOGFILE
    python3 -m pip install -U jetson-stats
fi
echo "##### Creating required folders" | sudo tee -a $LOGFILE
mkdir -p /opt/eyeflow/monitor/lib
if [ -e /opt/eyeflow/monitor/promtail/promtail* ] is present; then
    rm -R /opt/eyeflow/monitor/promtail
fi
mkdir -p /opt/eyeflow/monitor/promtail/positions
if ls /opt/eyeflow/monitor/collector-config-v4.yaml 1> /dev/null 2>&1; then
    echo "##### saving existing collector-config-v4 as collector-config-v4.bak" | sudo tee -a $LOGFILE
    mv /opt/eyeflow/monitor/collector-config-v4.yaml /opt/eyeflow/install/collector-config-v4.bak
fi
if ls /opt/eyeflow/monitor/collector-config-v5.yaml 1> /dev/null 2>&1; then
    echo "##### saving existing collector-config-v5 as collector-config-v5.bak" | sudo tee -a $LOGFILE
    mv /opt/eyeflow/monitor/collector-config-v5.yaml /opt/eyeflow/install/collector-config-v5.bak
fi
echo "##### Cloning Edge repo and set rights" | sudo tee -a $LOGFILE
cd /opt/eyeflow/install
rm -rf /opt/eyeflow/install/agent
git clone https://github.com/snsergio/agent.git
if id "eyeflow" >/dev/null 2>&1; then
    chown -R eyeflow:users /opt/eyeflow/monitor
else
    echo "##### User eyeflow not present" | sudo tee -a $LOGFILE
fi
setfacl -dm u::rwx,g::rwx,o::rx /opt/eyeflow/monitor
chmod g+rwxs /opt/eyeflow/monitor
chmod 775 /opt/eyeflow/monitor
rm -rf /opt/eyeflow/install/agent/install*
rm -rf /opt/eyeflow/install/agent/README*
rm -rf /opt/eyeflow/install/agent/stack
rsync -zvrh /opt/eyeflow/install/agent/* /opt/eyeflow/monitor
if ls /opt/eyeflow/install/collector-config-v4.bak 1> /dev/null 2>&1; then
    echo "##### returning existing collector-config-v4 to monitor as collector-config-v4.bak" | sudo tee -a $LOGFILE
    mv /opt/eyeflow/install/collector-config-v4.bak /opt/eyeflow/monitor/collector-config-v4.bak
fi
if ls /opt/eyeflow/install/collector-config-v5.bak 1> /dev/null 2>&1; then
    echo "##### previous collectot-config-v5 is present" | sudo tee -a $LOGFILE
    echo "##### move new collectot-config-v5 to .source" | sudo tee -a $LOGFILE
    echo "##### restoring previous collectot-config-v5 " | sudo tee -a $LOGFILE
    mv /opt/eyeflow/monitor/collector-config-v5.yaml /opt/eyeflow/monitor/collector-config-v5.source
    mv /opt/eyeflow/install/collector-config-v5.bak /opt/eyeflow/monitor/collector-config-v5.yaml
fi
echo "##### Preparing Promtail" | sudo tee -a $LOGFILE
cd /opt/eyeflow/monitor/promtail
curl -O -L "https://github.com/grafana/loki/releases/download/v2.4.1/promtail-linux-amd64.zip"
unzip "promtail-linux-amd64.zip"
sudo chmod a+x "promtail-linux-amd64"
sudo rm -R promtail-linux-amd64.zip
echo "##### Cloning Promtail Files" | sudo tee -a $LOGFILE
wget https://raw.githubusercontent.com/snsergio/agent/main/promtail/promtail-config.yml
wget https://raw.githubusercontent.com/snsergio/agent/main/promtail/promtail.service
echo "##### Copying promtail service to systemd" | sudo tee -a $LOGFILE
cp /opt/eyeflow/monitor/promtail/promtail.service /etc/systemd/system/. 
systemctl enable promtail.service 
echo "##### Preparing Promtail user and rights" | sudo tee -a $LOGFILE
if id "promtail" >/dev/null 2>&1; then
    echo "##### User Promtail already present" | sudo tee -a $LOGFILE
else
    useradd --system promtail
fi
usermod -a -G adm promtail
usermod -a -G systemd-journal promtail
setfacl -R -m u:promtail:rwx /opt/eyeflow/monitor/promtail/
echo "##### back to monitor configuration file" | sudo tee -a $LOGFILE
cd /opt/eyeflow/monitor
echo "##### Copying metric collector service to systemd" | sudo tee -a $LOGFILE
cp /opt/eyeflow/monitor/metric-collector.service /etc/systemd/system/. 
if ls /opt/eyeflow/monitor/collector-config-v5.source 1> /dev/null 2>&1; then
    echo "##### previous collectot-config-v5 is present" | sudo tee -a $LOGFILE
    echo "##### reloading systemctl daemon" | sudo tee -a $LOGFILE
    echo "##### restarting metric-collector" | sudo tee -a $LOGFILE
    systemctl daemon-reload
    systemctl restart metric-collector.service
fi
systemctl enable metric-collector.service 
echo "##### Remove temporary files" | sudo tee -a $LOGFILE
if [ -f /home/eyeflow/install-monitor.sh ]; then
    rm -f /home/eyeflow/install-monitor.sh
fi
if [ -f /home/eyeflow/install-edge.sh ]; then
    rm -f /home/eyeflow/install-edge.sh
fi
if [ -f /opt/eyeflow/monitor/install/install-monitor.sh ]; then
    rm -f /opt/eyeflow/monitor/install/install-monitor.sh
fi
files=(/home/eyeflow/README*)
if [ -e "${files[0]}" ]; then
    rm -R /home/eyeflow/README*
fi
files=(/opt/eyeflow/monitor/README*)
if [ -e "${files[0]}" ]; then
    rm -R /opt/eyeflow/monitor/README*
fi
files=(/opt/eyeflow/monitor/install*)
if [ -e "${files[0]}" ]; then
    rm -R /opt/eyeflow/monitor/install*
fi
rm -rf /opt/eyeflow/monitor/install/agent
echo "###########################################################" | sudo tee -a $LOGFILE
echo "#####   end of Metric Collector installation script   #####" | sudo tee -a $LOGFILE
echo "##### Finished at: $(date)" | sudo tee -a $LOGFILE
if [ ! -f /opt/eyeflow/install/edge-install.log ]; then
    mv $LOGFILE /opt/eyeflow/install/monitor-install-$(date +%F-%H:%M).log
    echo "####################################################################"
    echo "# LOG file at: /opt/eyeflow/install/monitor-install<date time>.log #"
    echo "####################################################################"
fi
echo "#################################################################################"
echo "# Edit Monitoring Agent configuration file to reflect Edge Station requirements #"
echo "#################################################################################"
echo "#     nano collector-config-v5.yaml                                             #"
echo "#     Then run:                                                                 #"
echo "#         systemctl start metric-collector.service  # To start metric collector #"
echo "#         systemctl status metric-collector.service # To check collector status #"
echo "#################################################################################"
echo " "
echo "#################################################################################"
echo "# Edit Promtail configuration file to reflect Edge Station requirements         #"
echo "#################################################################################"
echo "#     cd /opt/eyeflow/monitor/promtail                                          #"
echo "#     nano promtail-config.yml                                                  #"
echo "#     Then run:                                                                 #"
echo "#         systemctl start promtail.service  # To start metric collector         #"
echo "#         systemctl status promtail.service # To check collector status         #"
echo "#################################################################################"
echo " "
echo "#################################################################################"
echo "# After editing files, please REBOOT the system                                 #"
echo "#################################################################################"
