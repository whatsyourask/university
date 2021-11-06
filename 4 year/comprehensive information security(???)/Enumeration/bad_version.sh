#!/bin/bash

green='\033[0;32m'
clear='\033[0m'

function check_arg() {
  if [ -z $1 ]
  then
    printf "Usage:\n\t./enumeration.sh target\n"
    exit
  fi
}

function find_ips() {
  ips=($(nslookup $1 | grep -E "Address: ([0-9]{1,3}\.){3}([0-9]{1,3})" | cut -f2 -d' ' | tr '\n' ' '))
  if [ ${#ips[@]} -gt 1 ]
  then
    printf "[IP address]:"
    for ip in ${ips[@]};
    do
      printf "\n\t${green}${ip}${clear}"
    done
    printf "\n"
  else
    printf "[IP address]:\n\t${green}${ips}${clear}\n"
  fi
}

function find_net_range() {
  net_ranges=($(whois $1 | grep "NetRange: " | cut -d' ' -f8-10))
  if [ ${#net_ranges[@]} == 0 ]
  then
    net_range=($(whois $1 | grep "inetnum: " | cut -d' ' -f8-11))
    printf "simple"
    printf "\t${green}${net_range[$i]}"
    printf "\t\n"
  else
    #printf "hard"
    for net_range in ${net_ranges[@]};
    do
      net_range_len=${#net_range[@]}
      i=0
      diff=2
      while [[ $i -lt $net_range_len ]]; do
        new_net_range=(${new_net_range[@]} ${net_range[$i]})
        # printf "${clear}${net_range[$i]}"
        # printf "\t${green}${net_range[$i]}"
        printf "\n${net_range[$i]}"
        i=$i+$diff
        if [ $diff == 2 ]
        then
          diff=1
          #printf " - "
        else
          diff=2
          printf "\t\n"
        fi
      done
      #printf "\n"
    done
    printf "\n"
  fi
}

domain=$1
check_arg $domain
printf "Script started enumeration on ${green}${domain}${clear}\n\n"
find_ips $domain
printf "[IP ranges]:\n"
for ip in ${ips[@]};
do
  find_net_range $ip
done
