#!/usr/bin/env python3
import socket
import argparse
import re
from colorama import Fore
import socket


class Scanner:
    '''
    Class to scan TCP and UDP ports
    '''
    RECV_LEN = 4096
    def __init__(self, type, targets, ports, timeout):
        self.type = type
        self.targets = targets
        self.ports = ports
        self.timeout = timeout

    def _tcp_scan(self):
        # For each ips for each port connect and check timeout
        self.opened_ports = {}
        for target in self.targets:
            self.opened_ports[target] = []
            for port in self.ports:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.settimeout(self.timeout / 1000)
                    try:
                        s.connect((target, port))
                        self.opened_ports[target].append(port)
                    except:
                        continue
        self.pretty_output('tcp')

    def _udp_scan(self):
        # As with tcp scan, but also try to send and receive some data
        self.opened_ports = {}
        message = 'ping'
        for target in self.targets:
            self.opened_ports[target] = []
            for port in self.ports:
                # First method, didn't work out
                # with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
                #     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                #     s.settimeout(self.timeout / 1000)
                #     sock1 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                #     try:
                #         s.sendto(message.encode('utf-8'), (target, port))
                #         sock1.settimeout(1)
                #         data, addr = sock1.recvfrom(self.RECV_LEN)
                #         if data:
                #             self.opened_ports[target].append(port)
                #     except socket.timeout:
                #         serv = self.get_service_name(port, 'udp')
                #         if not serv:
                #             pass
                #         else:
                #             self.opened_ports[target].append(port)
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.settimeout(self.timeout / 1000)
                    try:
                        s.connect((target, port))
                        s.send(b' \r\n ')
                        data = s.recv(self.RECV_LEN)
                        print(data)
                        if data:
                            self.opened_ports[target].append(port)
                    except:
                        continue
        self.pretty_output('udp')

    def get_service_name(self, port, proto):
        # try to determine a service based on port number
        try:
            name = socket.getservbyport(int(port), proto)
        except:
            return None
        return name

    def pretty_output(self, proto):
        # Output in nmap-style.
        for host in self.opened_ports.keys():
            print(f'Scan report for {host}\n')
            if len(self.opened_ports[host]) > 0:
                print("PORT    STATE   SERVICE")
                for port in self.opened_ports[host]:
                    service = self.get_service_name(port, proto)
                    if service:
                        print(f'{port}/tcp  open    {service}')
                    else:
                        print(f'{port}/tcp  open')
                print()
            else:
                print('All ports are closed.\n')

    def run(self):
        # run scan based on type
        if self.type == 'T':
            self._tcp_scan()
        else:
            self._udp_scan()


def create_ports_range(ports):
    # to create a list of ports
    start, end = map(int, ports.split('-'))
    return [port for port in range(start, end + 1)]


def create_ip_range(ip_start, ip_end):
    # to create a list of ip from start to end
    ip_list = ip_start.split('.')
    start_last_octet = int(ip_list[-1])
    end_last_octet = int(ip_end.split('.')[-1])
    ip = ip_list[:-1]
    targets = []
    for i in range(start_last_octet, end_last_octet + 1):
        target = ip.copy()
        target.append(str(i))
        targets.append('.'.join(target))
    return targets


def validate_ips(ip_start, ip_end):
    check_targets = '(\d{1,3}\.){3}(\d{1,3})'
    start_res = re.search(check_targets, ip_start)
    end_res = re.search(check_targets, ip_end)
    if not start_res or not end_res:
        raise Exception(Fore.RED + '\n[!] Invalid IP address or IP range.\n')


def validate_ports(ports):
    range = ports.split('-')
    check_length = int(range[0]) > int(range[1])
    check_each_length = len(range[0]) > 5 or len(range[1]) > 5
    if check_length or check_each_length:
        raise Exception(Fore.RED + '\n\n[!] Invalid ports range.\n')


def validate_args(ip_start, ip_end, ports):
    # check ports for example
    # also tried to verify ips, but then decided not to do so
    validate_ports(ports)


def parse_args():
    # To create interface for cli tool
    parser = argparse.ArgumentParser(prog='portscan.py',
                                     usage='',
                                     description='Port scanner like nmap.',
                                     epilog='Written by whatsyourask.')
    parser.add_argument('-s', required=False, help='Type of scan.', choices=['T', 'U'], type=str)
    parser.add_argument('-rS', required=True, help='Start of IP range.', metavar='IP-address')
    parser.add_argument('-rE', required=True, help='End of IP range.', metavar='IP-address')
    parser.add_argument('-p', required=False, help='Ports range.', metavar='PORTS', default='1-1000')
    parser.add_argument('-t', required=False, help='Timeout.', metavar='TIMEOUT', default='100', type=int)
    argv = vars(parser.parse_args())
    return argv['s'], argv['rS'], argv['rE'], argv['p'], argv['t']


def main():
    type, ip_start, ip_end, ports, timeout = parse_args()
    validate_args(ip_start, ip_end, ports)
    targets = create_ip_range(ip_start, ip_end)
    ports = create_ports_range(ports)
    #print(targets)
    scanner = Scanner(type, targets, ports, timeout)
    scanner.run()


if __name__=='__main__':
    main()
