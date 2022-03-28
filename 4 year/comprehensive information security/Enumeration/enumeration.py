#!/usr/bin/env python3
import sys
from whois import query
from ipwhois import IPWhois
from socket import gethostbyname
from colorama import Fore
from nmap import PortScanner
import requests
import threading
import argparse


def get_ip_addr(domain_name, output_buf):
    ip = gethostbyname(domain_name)
    print(f'\n[IP address]:\n\t{Fore.GREEN}{ip}{Fore.RESET}\n')
    output_buf.append(f'\n[IP address]:\n\t{ip}\n')
    return ip


def list_print(desc, items, output_buf):
    print(desc)
    output_buf.append(desc)
    for item in items:
        print(f'\t{Fore.GREEN}{item}{Fore.RESET}')
        output_buf.append(f'\t{item}')
    print()
    output_buf.append('')


def get_info_by_name(domain_name, output_buf):
    info = query(domain_name).__dict__
    name_servers = info['name_servers']
    list_print('Name servers:', name_servers, output_buf)


def get_info_by_ip(ip, output_buf):
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
    list_print('Emails:', emails, output_buf)
    list_print('Subnets:', subnets, output_buf)
    return subnets


def scan_subnet(subnet, output_buf):
    ps = PortScanner()
    scan_result = ps.scan(subnet, arguments='-sn -PEPM -T4 --min-rate=1000 -n')
    #print(f'Live hosts for {Fore.GREEN}{subnet}{Fore.RESET}')
    uphosts = list(scan_result['scan'].keys())
    # dns_names = [scan_result['scan'][uphost]['hostnames'][0]['name'] for uphost in uphosts ]
    # print(dns_names)
    list_print(f'Live hosts for {subnet}', uphosts, output_buf)


def scan_subnets(subnets, output_buf):
    max_cidr = 0
    small_subnet = None
    for subnet in subnets:
        cidr = int(subnet.split('/')[1])
        if cidr > max_cidr:
            max_cidr = cidr
            small_subnet = subnet
    scan_subnet(small_subnet, output_buf)


def thread_request(subdomain, domain_name, output_buf):
    try:
        #print(subdomain)
        r = requests.get(f'https://{subdomain}.{domain_name}/', timeout=10)
        if r.status_code == requests.codes.ok:
            print(f'\t{Fore.GREEN}[+] {subdomain}.{domain_name}{Fore.RESET}')
            output_buf.append(f'\t[+] {subdomain}.{domain_name}')
    except:
        pass


def scan_subdomains(domain_name, output_buf):
    subdomains_list_url = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt'
    subdomains_top20000 = requests.get(subdomains_list_url).content.decode().split()
    print(f'Subdomains for {domain_name}')
    output_buf.append(f'Subdomains for {domain_name}')
    threads = []
    list_length = len(subdomains_top20000)
    for i in range(list_length):
        thread = threading.Thread(target=thread_request, args=(subdomains_top20000[i], domain_name, output_buf))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print()
    output_buf.append('')


def scan_ports(target, output_buf):
    try:
        #print(f'Scanning ports for {target}')
        ps = PortScanner()
        scan_result = ps.scan(target, arguments='-sT -T4 -Pn -n -p-')
        #print(scan_result)
        open_ports = scan_result['scan'][target]['tcp'].keys()
        list_print(f'Open TCP ports for {target}', open_ports, output_buf)
    except:
        scan_ports(target, output_buf)


def parse_args():
    parser = argparse.ArgumentParser(prog='enumeration.py',
                                     usage='./enumeration.py <target>',
                                     description='Tool to enumerate organization by its domain name.',
                                     epilog='Written by whatsyourask.')
    parser.add_argument('-t', required=True, help='Target to scan', type=str)
    parser.add_argument('-o', required=True, help='Filename where to write output', type=str)
    argv = vars(parser.parse_args())
    return argv['t'], argv['o']


def enumeration():
    domain_name, filename = parse_args()
    output_buf = []
    print(f'\n[!] Started enumeration for {Fore.GREEN}{domain_name}{Fore.RESET}')
    output_buf.append(f'\n[!] Started enumeration for {domain_name}')
    ip = get_ip_addr(domain_name, output_buf)
    get_info_by_name(domain_name, output_buf)
    subnets = get_info_by_ip(ip, output_buf)
    scan_subnets(subnets, output_buf)
    scan_subdomains(domain_name, output_buf)
    scan_ports(ip, output_buf)
    open(filename, 'w').write('\n'.join(output_buf))


if __name__=='__main__':
    enumeration()
