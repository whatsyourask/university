from socket import *
from crypto import *
import sys


class AuthServer:
    """
    Provides server functionality
    Like interface to work with socket and auth module
    """
    def start(self, address: str, port: int, bits_length: int) -> None:
        """Start the server"""
        # Creata a socket object
        self.__socket = socket(AF_INET, SOCK_STREAM)
        # Bind it to specified address and port
        self.__socket.bind((address, port))
        print('Listening...')
        # Start to listen
        self.__socket.listen()
        # Accept a new connection
        conn, addr = self.__socket.accept()
        print(f'Connection from {addr[0]}:{addr[1]}.')
        client_pub_key = conn.recv(1024)
        #print(client_pub_key)
        print('Client\'s public key received')
        rsa, pub_key, priv_key = generate_keys(bits_length)
        self.__rsa = rsa
        self.__pub_key = pub_key
        self.__priv_key = priv_key
        conn.send(str(pub_key).encode('utf-8'))


def main():
    try:
        a_server = AuthServer()
        port = int(sys.argv[1])
        bits_length = int(sys.argv[2])
        a_server.start('', port, bits_length)
    except ValueError:
        print('Usage: python3 server.py <port> <key bits length>')


if __name__=='__main__':
    main()
