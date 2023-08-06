#!/bin/bash
# Script for StartFailDns

# Block all traffic on port 53
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.7
iptables -I FORWARD -p tcp --sport 1024:65535 -d 10.56.32.199 --dport 53 -m tcp -j DROP
iptables -I FORWARD -p udp --sport 1024:65535 -d 10.56.32.199 --dport 53 -m udp -j DROP
