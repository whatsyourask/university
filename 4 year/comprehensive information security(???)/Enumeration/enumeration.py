#!/usr/bin/env python3
import sys
from whois import query
from ipwhois import IPWhois
from socket import gethostbyname
from colorama import Fore
from nmap import PortScanner
import requests


def get_ip_addr(domain_name):
    ip = gethostbyname(domain_name)
    print(f'\n[IP address]:\n\t{Fore.GREEN}{ip}{Fore.RESET}\n')
    return ip


def list_print(desc, items):
    print(desc)
    for item in items:
        print(f"\t{Fore.GREEN}{item}{Fore.RESET}")
    print()


def get_info_by_name(domain_name):
    info = query(domain_name).__dict__
    name_servers = info['name_servers']
    list_print('Name servers:', name_servers)


def get_info_by_ip(ip):
    obj = IPWhois(ip)
    info = obj.lookup_whois()
    #rint(info)
    nets = info['nets']
    subnets = []
    emails = []
    for net in nets:
        subnet = net['cidr']
        if subnet.find(',') > 0:
            temp = subnet.split(', ')
            for item in temp:
                subnets.append(item)
        else:
            subnets.append(subnet)
        email = net['emails']
        if len(email) > 1:
            for item in email:
                if item not in emails:
                    emails.append(item)
        elif email not in emails:
            emails.append(email)
    list_print('Emails:', emails)
    list_print('Subnets:', subnets)
    return subnets


def scan_subnet(subnet):
    ps = PortScanner()
    scan_result = ps.scan(subnet, arguments='-sn -PEPM -T4 --min-rate=1000 -n')
    print(f'Live hosts for {Fore.GREEN}{subnet}{Fore.RESET}')
    uphosts = list(scan_result['scan'].keys())
    # dns_names = [scan_result['scan'][uphost]['hostnames'][0]['name'] for uphost in uphosts ]
    # print(dns_names)
    list_print('UP hosts:', uphosts)


def scan_subnets(subnets):
    max_cidr = 0
    small_subnet = None
    for subnet in subnets:
        cidr = int(subnet.split('/')[1])
        if cidr > max_cidr:
            max_cidr = cidr
            small_subnet = subnet
    scan_subnet(small_subnet)


def thread_request(subdomain, domain_name):
    ...


def scan_subdomains(domain_name):
    subdomains_list_url = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-20000.txt'
    subdomains_top20000 = requests.get(subdomains_list_url).content.decode().split()
    #print(subdomains_top20000)
    print(f'Subdomains for {domain_name}')
    for subdomain in subdomains_top20000:
        try:
            r = requests.get(f'https://{subdomain}.{domain_name}/')
            if r.status_code == requests.codes.ok:
                print(f'\t{Fore.GREEN}[+] {subdomain}.{domain_name}')
        except:
            continue


def scan_ports(target):
    ...

    
def enumeration():
    if len(sys.argv) < 2:
        print(f'Usage:\n\t{Fore.BLUE}./enumeration.py <target>')
        exit()
    domain_name = sys.argv[1]
    print(f'\n[!] Started enumeration for {Fore.GREEN}{domain_name}{Fore.RESET}')
    ip = get_ip_addr(domain_name)
    get_info_by_name(domain_name)
    subnets = get_info_by_ip(ip)
    #scan_subnets(subnets)
    scan_subdomains(domain_name)


if __name__=='__main__':
    enumeration()
