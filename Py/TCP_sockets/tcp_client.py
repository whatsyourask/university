from socket import *

# set a server name and port
server_name = '10.0.2.15'
server_port = 12666
# create client socket with IPv4 and TCP
client_socket = socket(AF_INET, SOCK_STREAM)
# Connect to server
client_socket.connect((server_name, server_port))
# Input data
sentence = input('Input lowercase sentence:')
# Send to server by means of client socket
client_socket.send(bytes(sentence,encoding = 'utf-8'))
# Receive data from server
modified_sentence = client_socket.recv(1024)
print('From Server:',modified_sentence)
client_socket.close()
