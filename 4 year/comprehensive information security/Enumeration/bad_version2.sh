#!/bin/bash

green='\033[0;32m'
clear='\033[0m'
yellow='\033[0;33m'

function check_arg() {
  if [ -z $1 ]
  then
    printf "Usage:\n\t./enumeration.sh <target>\n"
    exit
  fi
}

function print_ip_addresses() {
  for ip in ${ip_addresses[@]};
  do
    printf "\n${green}${ip}${clear}"
  done;
  printf "\n"
}

function get_ips() {
  ip_addresses=($(nslookup $1 | grep -E "Address: ([0-9]{1,3}\.){3}([0-9]{1,3})" | cut -f2 -d' ' | tr '\n' ' '))
  if [ ${#ip_addresses[@]} -gt 1 ]
  then
    printf "$yellow[IP addresses]:$clear"
    print_ip_addresses
  else
    printf "$yellow[IP address]:\n${green}${ip_addresses}${clear}\n"
  fi
}

function get_emails() {
  emails=$(whois $1 | grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b" | uniq)
  printf "\nEmails:\n"
  printf "${green}${emails}${clear}"
  printf "\n"
}

function get_ns() {
  ns=$(whois $1 | grep -E "Name Server: " | grep -P "([A-Za-z0-9-])+\.([A-Za-z0-9-])+\.([A-Za-z0-9-])+" -o | uniq -i)
  printf "\nName servers:\n"
  printf "${green}${ns}${clear}\n"
}

function get_ports() {
  nmap_results=$(nmap -sT -T4 -Pn --min-rate=1000 $1 | grep open)
  printf "\nNmap scan:\n"
  printf "$green$nmap_results$clear\n"
}

function get_subnet() {
  subnet=$(whois $1 | grep -P "([0-9]{1,3}\.){3}[0-9]{1,3}\/[0-9]{1,2}" -o)
  live_hosts=$(sudo nmap -PEPM -T4 --min-rate=1000 $subnet)
  printf "Live hosts:\n"
  printf "$live_hosts\n"
}

# function netdiscover() {
#
# }

target=$1
check_arg $target
printf "\n[!] Script started enumeration on ${green}${target}${clear}...\n\n"
declare -a ip_addresses
get_ips $target
printf "$yellow\n[whois information for $green${target}$clear]:\n"
get_emails $target
get_ns $target
for ip in ${ip_addresses[@]};
do
  printf "\n$yellow[Information about ${green}${ip}${clear}]\n"
  get_emails $ip
  get_ports $ip
  get_subnet $ip
done
