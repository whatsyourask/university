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
        print('[+] Connection established.')

    def authenticate(self, login: str=None, password: str=None) -> None:
        """Entire authentication"""
        # Begin a stage one
        continue_auth = self._auth_stage1()
        if continue_auth:
            # If it did okay, go to stage two
            print('[+] Server\'s public key received.')
            if not login and not password:
                self.__login = input('Login: ')
                self.__password = input('Password: ')
            else:
                self.__login = password
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
        self.__server_pub_key = server_pub_key
        return super()._check_the_key(server_pub_key)

    def _auth_stage2(self) -> str:
        """Encrypt the login:password and send it"""
        hash = super().get_hash(self.__password)
        account = self.__login.encode(self.ENCODING) + b'\n' + hash
        self.__server_pub_key = super()._get_key(self.__server_pub_key)
        encrypted = super().encrypt_twice(self.__server_pub_key, account)
        return encrypted

    def _auth_stage3(self, encrypted: str) -> str:
        super().sendall(self.__socket, str(encrypted))
        encrypted_response = super().recvall(self.__socket)
        print(encrypted_response)
        response = super().decrypt_twice(self.__server_pub_key, encrypted_response)
        print('response: ', response.decode(super().ENCODING))
        if response == super().SUCCESS:
            print('Nice.')
        if response == super().FAILURE:
            print('Not nice...')


def main():
    try:
        port = int(sys.argv[1])
        bits_length = int(sys.argv[2])
        a_client = AuthClient('', port, bits_length)
        a_client.connect()
        a_client.authenticate()
    except ValueError:
        print('Usage: \n\tpython3 client.py <port> <key bits length>')
    # port = int(sys.argv[1])
    # bits_length = int(sys.argv[2])
    # a_client = AuthClient('', port, bits_length)
    # a_client.connect()
    # a_client.authenticate('user', 'password')


if __name__=='__main__':
    main()
