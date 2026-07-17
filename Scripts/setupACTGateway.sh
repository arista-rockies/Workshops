#!/bin/bash

# start with some cleanup and installing new required packages
echo "starting yum steps `date`"

#yum clean all
#yum -y update
yum -y install git kea wget iptables-services tcpdump iftop

# these two lines make the rest of the current bootstrap work properly
ip addr add 100.64.0.1/32 dev lo
ip addr add 10.0.96.20/32 dev lo

echo "setting up system daemons `date`"

# re-configure ntp and restart it
echo "allow 192.168.0.0/22" >> /etc/chrony.conf

cat <<EOF > /etc/systemd/system/bootstrap.service
[Unit]
Description=Arista Bootstrap Server
After=network.target
StartLimitInterval=300s
StartLimitBurst=8

[Service]
Type=simple
ExecStart=/home/administrator/Projects/Workshops/Scripts/.venv/bin/uvicorn bootstrap:app --reload --host 0.0.0.0 --reload-exclude "tmp/*" --port 8000
WorkingDirectory=/home/administrator/Projects/Workshops/Scripts
User=administrator
SyslogIdentifier=bootstrap
Restart=always
RestartSec=30s

[Install]
WantedBy=default.target
EOF

cat <<EOF > /etc/kea/kea-dhcp4.conf
{
"Dhcp4": {
    "interfaces-config": {
        "interfaces": [ "tun0" ]
    },

    "control-socket": {
        "socket-type": "unix",
        "socket-name": "/tmp/kea4-ctrl-socket"
    },

    "lease-database": {
        "type": "memfile",
        "lfc-interval": 3600
    },

    "expired-leases-processing": {
        "reclaim-timer-wait-time": 10,
        "flush-reclaimed-timer-wait-time": 25,
        "hold-reclaimed-time": 3600,
        "max-reclaim-leases": 100,
        "max-reclaim-time": 250,
        "unwarned-reclaim-cycles": 5
    },

    "renew-timer": 900,
    "rebind-timer": 1800,
    "valid-lifetime": 3600,

    "option-data": [
        {
            "name": "domain-name-servers",
            "data": "1.1.1.1"
        },

        {
            "code": 15,
            "data": "arista.local"
        },

        {
            "name": "domain-search",
            "data": "arista.local"
        },
        {
            "name": "default-ip-ttl",
            "data": "0xf0"
        },
        {
            "name": "boot-file-name",
            "data": "http://192.168.0.1:8000/bootstrap.py"
        }
    ],

    "subnet4": [
        {
            "subnet": "192.168.0.0/22",
            "pools": [ { "pool": "192.168.1.0 - 192.168.2.254" } ],

            "option-data": [
                {
                    "name": "routers",
                    "data": "192.168.0.1"
                }
            ]
        }
    ],

    "loggers": [
    {
        "name": "kea-dhcp4",
        "output_options": [
            {
                "output": "/var/log/kea-dhcp4.log"
            }
        ],
        "severity": "INFO",
        "debuglevel": 0
    }
  ]
}
}
EOF

cat << EOF > /etc/sysctl.d/98-forwarding.conf
net.ipv4.ip_forward = 1
EOF

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
/usr/libexec/iptables/iptables.init save

systemctl daemon-reload
systemctl disable firewalld
systemctl enable kea-dhcp4 iptables bootstrap

echo "disabling selinux `date`"

# disable selinux
sed -i 's/=enforcing/=disabled/' /etc/selinux/config

echo "starting administrator steps"

# from here on out, these commands need to run as administrator
sudo -i -u administrator bash << EOF
	mkdir Projects
	cd Projects

	# clone the workshop scripting
	echo "cloning `date`"
	git clone https://github.com/arista-rockies/Workshops

	echo "installing uv `date`"
	# install uv as this is the easiest way to get a recent python
	curl -LsSf https://astral.sh/uv/install.sh | sh

	# configure uv
	echo "configuring uv `date`"
	cd Workshops/Scripts
	uv python install 3.14.0
	uv python pin 3.14.0
	uv venv --clear
	uv pip compile requirements.txt --universal --output-file requirements.txt.new
	uv pip sync requirements.txt.new

	# for our benefit i'm going to add a symlink where it shouldn't be
	ln -s /home/administrator/Projects/Workshops/Scripts/.venv /home/administrator/Projects/Workshops/Scripts/venv

EOF

echo "moving the tokenConfig `date`"
mv /home/administrator/tokenConfig.yml /home/administrator/Projects/Workshops/Scripts/

echo "chowning `date`"
chown -R administrator:administrator /home/administrator/

echo "trying reboot `date`"
/sbin/shutdown -r +1 rebooting in 1m
exit

#echo "ensure you copy a valid tokenConfig.yml onto the server and reboot!"
