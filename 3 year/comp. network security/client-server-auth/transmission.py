class Transmission:
    ENCODING = 'utf-8'
    BUF_SIZE = 1024
    def recvall(self, conn) -> str:
        buff = b''
        temp = conn.recv(self.BUF_SIZE)
        received = len(temp)
        while received:
            temp = conn.recv(self.BUF_SIZE)
            received = len(temp)
            print(received)
            if not received:
                raise RuntimeError('Connection broken.')
            buff += temp
            print(temp)
        return buff.decode(self.ENCODING)

    def sendall(self, conn, data: str) -> None:
        sent_length = 0
        data_length = len(data)
        while sent_length < data_length:
            sent = conn.send(data[sent_length:].encode(self.ENCODING))
            if not sent:
                raise RuntimeError('Connection broken.')
            sent_length += sent
