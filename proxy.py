#!/usr/bin/env python

# TCP Proxy
import argparse
import socket

import sys
import threading


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on {address}:{port}".format(address=local_host, port=local_port)
        print "[!!] Check for other listening sockets or correct permissions"
        sys.exit(0)

    print "[*] Listening on {address}:{port}".format(address=local_host, port=local_port)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # print out the local connection information
        print '[==>] Received incoming connection from {client_address}:{client_port}'.format(client_address=addr[0], client_port=addr[1])

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
def main():

    parser = argparse.ArgumentParser(description="TCP Proxy")
    parser.add_argument('localhost')
    parser.add_argument('localport')
    parser.add_argument('remotehost')
    parser.add_argument('remoteport')
    parser.add_argument('-r', '--receive_first', action=store_true, default=True)

    args = parser.parse_args()

    # setup local listening parameters
    local_host = args.localhost
    local_port = args.localport

    # setup remote target
    remote_host = args.remotehost
    remote_port = args.remoteport

    # this tells our proxy to connect and receive data before seing to the remote host
    if args.receive_first:
        receive_first = True
    else:
        receive_first = False

    # spin up listening socket
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == '__main__':
    main()
