from socket import *


# set server name and port
server_name = 'hostname'
server_port = 12663
# create a socket with IPv4 and we use UDP
client_socket = socket(AF_INET, SOCK_DGRAM)
# input message
message = bytes(input('Input lowercase sentence:'), encoding = 'utf-8')
# send message to server by means of client socket
client_socket.sendto(message, (server_name, server_port))
# buffer = 2048 byte
modified_message, server_address = client_socket.recvfrom(2048)
print(modified_message)
# close socket and process will be finished
client_socket.close()
