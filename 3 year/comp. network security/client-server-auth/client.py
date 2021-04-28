from auth import *
from socket import *
import sys
from transmission import *


class AuthClient(Auth, Transmission):
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

    def authenticate(self, login: str, password: str) -> None:
        """Entire authentication"""
        # Begin a stage one
        continue_auth = self._auth_stage1()
        if continue_auth:
            # If it did okay, go to stage two
            print('[+] Server\'s public key received.')
            self.__login = login
            self.__password = password
            encrypted = self._auth_stage2()
            self._auth_stage3(encrypted)
        else:
            self.__socket.close()

    def _auth_stage1(self) -> bool:
        """Keys generation and obtaining the key from the server"""
        super().generate_keys(self.__bits_length)
        super().sendall(self.__socket, str(self._pub_key))
        server_pub_key = super().recvall(self.__socket)
        print(server_pub_key)
        self.__server_pub_key = server_pub_key
        return super()._check_the_key(server_pub_key)

    def _auth_stage2(self) -> str:
        """Encrypt the login:password and send it"""
        hash = super().get_hash(self.__password)
        account = self.__login.encode(self.ENCODING) + b' ' + hash
        print(len(account))
        self.__server_pub_key = super()._get_key(self.__server_pub_key)
        encrypted = super().encrypt_twice(self.__server_pub_key, account)
        return encrypted

    def _auth_stage3(self, encrypted: str) -> str:
        super().sendall(self.__socket, str(encrypted))
        response = super().recvall(self.__socket)
        if response == 'Successfully logged in.':
            print('Nice.')


def main():
    try:
        port = int(sys.argv[1])
        bits_length = int(sys.argv[2])
        a_client = AuthClient('', port, bits_length)
        a_client.connect()
        a_client.authenticate('user', 'password')
    except ValueError:
        print('Usage: \n\tpython3 client.py <port> <key bits length>')
    # port = int(sys.argv[1])
    # bits_length = int(sys.argv[2])
    # a_client = AuthClient('', port, bits_length)
    # a_client.connect()
    # a_client.authenticate('user', 'password')


if __name__=='__main__':
    main()
