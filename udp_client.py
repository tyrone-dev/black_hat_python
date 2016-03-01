#!/usr/bin/env python

# udp client
# user datagram protocol
# connectionless, 2 tuple : (dest addr, dest port)


import socket

target_host = "127.0.0.1"
target_port = 80

# create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# af_intet - IPv4 ip address or hostname
# sock_dgram - UDP client

# send some data
client.sendto("Data to send here", (target_host, target_port))

# receive some data
data, addr = client.recvfrom(4096)
# returns received data and address (ip, port) of remote host

print data