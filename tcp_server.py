#!/usr/bin/env python

# standard multi-threaded TCP server
import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ip adress we want the server to listen on
server.bind((bind_ip, bind_port))

# tell the server to start listening with a maximum backlog of connections = 5
server.listen(5)

print '[*] Listening on %s:%d' % (bind_ip, bind_port)

# this is out client-handling thread
def handle_client(client_socket):
    """
    gets data from client socket and replies with an ACK
    :param client_socket: client socket to use for receiving and sending data
    :return: None
    """

    # print out what client sends
    request = client_socket.recv(1024)

    print '[*] Received: %s' % request

    # send packet back to client
    client_socket.send('ACK!')

    # close the socket
    client_socket.close()

# server always listens for clients & always waiting
while True:

    # when client connects: client is a client socket, addr = remote connection details
    client, addr = server.accept()

    print "[*] Accepted connection from: %s:%d" %(addr[0], addr[1])

    # create a new thread to handle the clients and the incoming data
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()  # start thread, server ready to handle another incoming connection or client