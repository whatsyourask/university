from auth import *
from socket import *
import sys


class AuthServer(Auth):
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
        self.__conn, addr = self.__socket.accept()
        print(f'Connection from {addr[0]}:{addr[1]}')
        # Begin a stage one
        continue_auth = self._auth_stage1()
        if continue_auth:
            # if it did okay, go to stage two
            print('[+] Client\'s public key received.')
            super()._generate_keys(bits_length)
            self.__conn.send(str(self._pub_key).encode(self.ENCODING))
        else:
            self.__socket.close()

    def _auth_stage1(self) -> bool:
        """Receive the client's key and check it"""
        client_pub_key = self.__conn.recv(1024).decode(self.ENCODING)
        print(client_pub_key)
        self.__client_pub_key = client_pub_key
        return super()._check_the_key(client_pub_key)

    def _auth_stage2(self):
        pass


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
