#!/bin/bash
# Script for EndFailDns

# Delete rules that block traffic on port 53

iptables -D FORWARD -p tcp --sport 1024:65535 -d 10.56.32.199 --dport 53 -m tcp -j DROP
iptables -D FORWARD -p udp --sport 1024:65535 -d 10.56.32.199 --dport 53 -m udp -j DROP
