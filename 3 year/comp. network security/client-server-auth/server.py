from socket import *


class AuthServer:
    """
    Provides server functionality
    Like interface to work with socket and auth module
    """
    def start(self, address: str, port: int) -> None:
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
        print(f'Connection from {addr[0]}:{addr[1]}')


def main():
    a_server = AuthServer()
    a_server.start('', 4444)


if __name__=='__main__':
    main()
