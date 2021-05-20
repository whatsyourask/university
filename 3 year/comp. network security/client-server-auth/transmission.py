from socket import timeout

class Transmission:
    ENCODING = 'utf-8'
    BUF_SIZE = 1024
    def recvall(self, conn) -> str:
        buff = []
        try:
            received = 0
            while received == self.BUF_SIZE or received == 0:
                temp = conn.recv(self.BUF_SIZE)
                received = len(temp)
                if not received:
                    break
                buff.append(temp)
            buff = b''.join(buff)
            return buff.decode(self.ENCODING)
        except timeout:
            buff = b''.join(buff)
            return buff.decode(self.ENCODING)

    def sendall(self, conn, data: str) -> None:
        try:
            sent_length = 0
            data_length = len(data)
            data = data.encode(self.ENCODING)
            while sent_length < data_length:
                sent = conn.send(data[sent_length:])
                sent_length += sent
        except timeout:
            return
