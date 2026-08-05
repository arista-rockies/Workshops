#!/bin/bash
case "$1" in
	add)
		iptables -I FORWARD -s 192.168.2.0/24 -j DROP
		;;
	del)
		iptables -D FORWARD -s 192.168.2.0/24 -j DROP
		;;
esac

/usr/libexec/iptables/iptables.init save
