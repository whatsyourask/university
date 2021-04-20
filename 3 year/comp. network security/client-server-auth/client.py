from socket import *


class AuthClient:
    """
    Provides client functionality
    Like interface to work with socket and auth module
    """
    def connect(self, addr: str, port: int) -> None:
        """Connect to a server"""
        # Create a socket object
        self.__socket = socket(AF_INET, SOCK_STREAM)
        # Check if it is a localhost
        is_localhost = addr == ''
        if is_localhost:
            # if it is then convert '' to localhost address
            addr = '127.0.0.1'
        print(f'Trying to connect to {addr}:{port}')
        # Connect to the server
        self.__socket.connect((addr, port))
        print('Connection established')


def main():
    a_client = AuthClient()
    a_client.connect('', 4444)


if __name__=='__main__':
    main()
