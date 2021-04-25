class Transmission:
    ENCODING = 'utf-8'
    BUF_SIZE = 1024
    def recvall(self, conn) -> str:
        buff = []
        received = 0
        while received == self.BUF_SIZE or received == 0:
            #print('RECEIVING')
            temp = conn.recv(self.BUF_SIZE)
            received = len(temp)
            if not received:
                break
            #print(received)
            buff.append(temp)
            #print(temp)
        buff = b''.join(buff)
        #print(buff.decode(self.ENCODING))
        return buff.decode(self.ENCODING)

    def sendall(self, conn, data: str) -> None:
        sent_length = 0
        data_length = len(data)
        data = data.encode(self.ENCODING)
        #print(len(data))
        while sent_length < data_length:
            #print('SENDING')
            sent = conn.send(data[sent_length:])
            #print('sent', sent)
            sent_length += sent
            #print('sent_length', sent_length)
            # if not sent:
            #     raise RuntimeError('Connection broken.')
        #print('sending completed')
