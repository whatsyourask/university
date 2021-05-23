#!/usr/bin/env bash

tcpdump -i any -vn dst port 80 -G 120 -W 1 -w ~/captured.pcap
tcpdump -nr captured.pcap | awk '{print $3,$6}' > captured.txt
# 0 * * * * ~/capture-in-2-minutes.sh
