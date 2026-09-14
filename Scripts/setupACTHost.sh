#!/bin/bash
set -euo pipefail

IP1="10.2.2.1"
IP2="10.2.2.2"
MAC="AE:53:EC:1D:FB:B2"

# start with some cleanup and installing new required packages
echo "starting yum steps `date`"

#yum clean all
#yum -y update
yum -y install git kea wget iptables-services tcpdump iftop

echo "setting up the network stack"
cat <<EOF >> /usr/sbin/act-network-create
echo " - leaf1c"
ip addr add ${IP1}/24 dev et11

echo " - leaf2a"
ip netns add leaf2a
ip link set dev et21 down
ip link set dev et21 netns leaf2a
ip -n leaf2a link set dev et21 address ${MAC}
ip -n leaf2a add add ${IP2}/24 dev et21
ip -n leaf2a link set dev et21 up

echo " - leafztr"
ip netns add leafztr
ip link set dev et22 down
ip link set dev et22 netns leafztr
ip -n leafztr link set dev et22 address ${MAC}
ip -n leafztr add add ${IP2}/24 dev et22
ip -n leafztr link set dev et22 up
EOF

cat <<EOF > /etc/systemd/system/pingjob.service
[Unit]
Description=ping job
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/sbin/ping ${IP2}
User=root
SyslogIdentifier=ping
Restart=always
RestartSec=5s

[Install]
WantedBy=default.target
EOF

systemctl daemon-reload
systemctl enable pingjob
systemctl start pingjob

