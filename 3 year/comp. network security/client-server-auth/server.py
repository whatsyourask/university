from auth import *
from socket import *
import sys
from transmission import *


class AuthServer(Auth, Transmission):
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
        self._get_accounts()
        # Start to listen
        self.__socket.listen()
        # Accept a new connection
        self.__conn, addr = self.__socket.accept()
        print(f'[+] Connection from {addr[0]}:{addr[1]}')
        # Begin a stage one
        continue_auth = self._auth_stage1()
        if continue_auth:
            # if it did okay, go to stage two
            print('[+] Client\'s public key received.')
            account = self._auth_stage2(bits_length)
            self._auth_stage3(account)
        else:
            self.__socket.close()

    def _auth_stage1(self) -> bool:
        """Receive the client's key and check it"""
        client_pub_key = super().recvall(self.__conn)
        self.__client_pub_key = client_pub_key
        return super()._check_the_key(client_pub_key)

    def _auth_stage2(self, bits_length: int) -> str:
        super().generate_keys(bits_length)
        super().sendall(self.__conn, str(self._pub_key))
        account = super().recvall(self.__conn)
        return account

    def _auth_stage3(self, account: str):
        self.__client_pub_key = super()._get_key(self.__client_pub_key)
        account = super().decrypt_twice(self.__client_pub_key, account).split(b'\n')
        print(self.__accounts.keys())
        print(account[0])
        print(account[0] not in self.__accounts.keys())
        if account[0] not in self.__accounts.keys():
            response = super().encrypt_twice(self.__client_pub_key, super().FAILURE)
            print(response)
            super().sendall(self.__conn, response)

    def _get_accounts(self):
        accounts = list(map(lambda user_pass: user_pass.split(b' '),
                        open('accounts.txt', 'rb').read().split(b'\n')))
        temp_dict = {}
        for item in accounts:
            if len(item) > 1:
                temp_dict[item[0]] = item[1]
        self.__accounts = temp_dict.copy()


def main():
    # try:
    #     a_server = AuthServer()
    #     port = int(sys.argv[1])
    #     bits_length = int(sys.argv[2])
    #     a_server.start('', port, bits_length)
    # except ValueError:
    #     print('Usage: python3 server.py <port> <key bits length>')
    a_server = AuthServer()
    port = int(sys.argv[1])
    bits_length = int(sys.argv[2])
    a_server.start('', port, bits_length)


if __name__=='__main__':
    main()
