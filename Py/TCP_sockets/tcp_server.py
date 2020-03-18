from socket import *


server_port = 12666
# Create server socket
server_socket = socket(AF_INET, SOCK_STREAM)
# Bind the port
server_socket.bind(('', server_port))
# Server is listening clients,count of clients is 1
server_socket.listen(1)
print('The server is ready to receive')
while 1:
    # Create a new socket for transfer data
    connection_socket, addr = server_socket.accept()
    sentence = connection_socket.recv(1024)
    capitalized_sentence = sentence.upper()
    # Send data to client by means of connection_socket
    connection_socket.send(capitalized_sentence)
    connection_socket.close()
