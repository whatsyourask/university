from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP


def send_packets(dst: str, dport: int, sport: int, protocol):
    for last_octet in range(100):
        send(IP(src=f'192.168.88.{last_octet}', dst=dst) / protocol(sport=sport, dport=dport))
        if last_octet == 50:
            for i in range(100):
                send(IP(src=f'192.168.88.{last_octet}', dst=dst) / protocol(sport=sport, dport=dport))


def main():
    dst = '127.0.0.1'
    dport = 80
    sport = 4444
    send_packets(dst, dport, sport, TCP)
    send_packets(dst, dport, sport, UDP)


if __name__=='__main__':
    main()
