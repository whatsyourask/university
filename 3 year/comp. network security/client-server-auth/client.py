from socket import *
from crypto import *
import sys


class AuthClient:
    """
    Provides client functionality
    Like interface to work with socket and auth module
    """
    def __init__(self, addr: str, port: int, bits_length: int) -> None:
        self.__addr = addr
        self.__port = port
        self.__bits_length = bits_length

    def connect(self) -> None:
        """Connect to a server"""
        # Create a socket object
        self.__socket = socket(AF_INET, SOCK_STREAM)
        # Check if it is a localhost
        is_localhost = self.__addr == ''
        if is_localhost:
            # if it is then convert '' to localhost address
            self.__addr = '127.0.0.1'
        print(f'Trying to connect to {self.__addr}:{self.__port}')
        # Connect to the server
        self.__socket.connect((self.__addr, self.__port))
        print('Connection established.')

    def authenticate(self, login: str, password: str):
        rsa, pub_key, priv_key = generate_keys(self.__bits_length)
        self.__rsa = rsa
        self.__pub_key = pub_key
        self.__priv_key = priv_key
        self.__socket.send(str(pub_key).encode('utf-8'))
        server_pub_key = self.__socket.recv(1024)
        # print(server_pub_key)
        print('Client\'s public key received')


def main():
    try:
        port = int(sys.argv[1])
        bits_length = int(sys.argv[2])
        a_client = AuthClient('', port, bits_length)
        a_client.connect()
        a_client.authenticate('user', 'password')
    except ValueError:
        print('Usage: python3 client.py <port> <key bits length>')


if __name__=='__main__':
    main()
