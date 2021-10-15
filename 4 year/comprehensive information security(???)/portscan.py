import socket
import argparse
import re
from colorama import Fore
import socket


class Scanner:
    RECV_LEN = 1024
    def __init__(self, type, targets, ports, timeout):
        self.type = type
        self.targets = targets
        self.ports = ports
        self.timeout = timeout

    def _tcp_scan(self):
        for target in self.targets:
            print('Scan report for ', target)
            for port in self.ports:
                #print(target, port)
                buf = b''
                try:
                    s = socket.create_connection((target, port), self.timeout // 1000)
                    s.sendall(b'AAAAA')
                    buf = s.recv(1024)
                    print(f'{port}/tcp open')
                except Exception:
                    print(f'{port}/tcp closed')
                    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    #     #print(target, port)
                    #     s.connect((target, port))
                    #     print(port, 'open')
                    #     s.settimeout(self.timeout // 1000)
                    #     s.send(b'AAAAAAAAAA')
                    #     buf = s.recv(self.RECV_LEN)
                    #     s.settimeout(None)

    def _udp_scan(self):
        ...

    def run(self):
        if self.type == 'T':
            self._tcp_scan()
        else:
            self._udp_scan()


def create_ports_range(ports):
    start, end = map(int, ports.split('-'))
    return [port for port in range(start, end + 1)]


def create_ip_range(ip_start, ip_end):
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
    validate_ips(ip_start, ip_end)
    validate_ports(ports)


def parse_args():
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
