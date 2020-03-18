from socket import *


server_port = 12663
server_socket = socket(AF_INET, SOCK_DGRAM)
# binding socket with port
server_socket.bind(('', server_port))
print("The server is ready to receive")
while 1:
    # Put data in message
    message, client_address = server_socket.recvfrom(2048)
    # Do operations with message
    modified_message = message.upper()
    # Send back to client by means of server socket
    server_socket.sendto(modified_message, client_address)
