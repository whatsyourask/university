from collections import Counter
from credentials import get_email, get_password
import asyncio
import smtplib
import email


def get_packets(filename: str) -> list:
    flags = 'Flags'
    packets = []
    wrong_udp = 'UDP,'
    with open(filename, 'r') as captured:
        while True:
            packet = captured.readline()
            if packet == '':
                break
            if flags in packet:
                packet = packet.replace(flags, 'TCP')
            if wrong_udp in packet:
                packet = packet.replace(wrong_udp, 'UDP')
            packets.append(packet)
    return packets


async def send_email_notification(smtp_server, admin_email: str, admin_password: str, message: str):
    try:
        print('\tSending email-notification to admin...')
        email_message = email.message.EmailMessage()
        email_message['Subject'] = 'Found DDoS attack.'
        email_message.set_content(message)
        smtp_server.send_message(email_message, admin_email, admin_email)
        print('\tNotification sent.')
    except Exception as error:
        print(f'\t[!] Notification sending error: {error}')


def create_smtp_conn(admin_email: str, admin_password: str):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_server = smtplib.SMTP(smtp_host, smtp_port)
    smtp_server.starttls()
    smtp_server.login(admin_email, admin_password)
    return smtp_server


def extract_packet_info(packet: str) -> tuple:
    packet = packet.split()
    sep_ind = packet[0].rfind('.')
    ip_address = packet[0][:sep_ind]
    port = packet[0][sep_ind + 1:]
    protocol = packet[1]
    return ip_address, port, protocol


async def search_ddos_attack(counted_packets: Counter, ddos_threshold: int):
    email = get_email()
    password = get_password()
    print(counted_packets)
    smtp_server = create_smtp_conn(email, password)
    for packet, packets_count in counted_packets.items():
        if packets_count >= ddos_threshold:
            print('[!] DDoS attack detected.')
            ip_address, port, protocol = extract_packet_info(packet)
            message = f'This {ip_address} IP address is doing DDoS attack on {protocol}/{port} in amount of {packets_count}.'
            await send_email_notification(smtp_server, email, password, message)
    smtp_server.quit()


def main():
    packets = get_packets('captured.txt')
    print(packets)
    counted_packets = Counter(packets)
    asyncio.run(search_ddos_attack(counted_packets, 100))


if __name__=='__main__':
    main()
