#!/bin/bash

green='\033[0;32m'

clear='\033[0m'

domain=$1

ip=$(nslookup $domain | grep -E "Address: ([0-9]{1,3}\.){3}([0-9]{1,3})" | cut -f2 -d' ')

printf "Script started enumeration on ${green}${domain}${clear}\n"

printf "\t[IP addres]: ${green}${ip}${clear}\n"

net_range=$(whois $ip | grep "NetRange: " | cut -d' ' -f8-10)

printf "\t[IP ranges]: ${green}${net_range}${clear}\n"
