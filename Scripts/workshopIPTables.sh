#!/bin/bash
addBlockCampusB() {
	iptables -A campusb -j DROP
}
addBlockL2() {
	iptables -A leaf2 -j DROP
}
addBlockZTR() {
	iptables -A ztr -j DROP
}
delBlockCampusB() {
	iptables -F campusb
}
delBlockL2() {
	iptables -F leaf2
}
delBlockZTR() {
	iptables -F ztr
}

case "$1" in
	reset)
		delBlockCampusB
		delBlockL2
		delBlockZTR

		addBlockCampusB
		addBlockL2
		addBlockZTR
		;;
	blockAll)
		addBlockCampusB
		addBlockL2
		addBlockZTR
		;;
	unBlockAll)
		delBlockCampusB
		delBlockL2
		delBlockZTR
		;;
	unBlockCampusB)
		delBlockCampusB
		delBlockL2
		;;
	unBlockZTR)
		addBlockL2
		delBlockZTR
		;;
esac

/usr/libexec/iptables/iptables.init save
