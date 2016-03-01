#!/usr/bin/env python

# a simple TCP Client
# transmission control protocol [Transport Layer]
# connection oriented, 4 tuple (dest addr, dest port, src addr, src port)

import socket

#target_host = "www.google.com"  # what we are connecting to
target_host = '0.0.0.0'
target_port = 9999  # port to use for connection

# create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# af_inet - IPv4 addres or hostname
# sock_stream - TCP

# connect the client
client.connect((target_host, target_port))

# # send some data
#client.send("GET /  HTTP/1.1\r\nHost: google.com\r\n\r\n")
client.send('ABCDEF')

# receive some data
response = client.recv(4096)

print response
