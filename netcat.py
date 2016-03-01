#!/usr/bin/env python
# python implementation of netcat

# define some global variables
import argparse
import socket

import sys

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to out target host
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

            while True:

                # wait for data back from client
                recv_len = 1
                response = ''

                while recv_len:

                    data = client.recv(4096)
                    recv_len = len(data)
                    response += data

                    if recv_len < 4096:
                        break

                print response,

                # wait for more inputs
                buffer = raw_input('')
                buffer += '\n'

                # send it off
                client.send(buffer)

    except:

        print '[*] Exception! Exiting'

        # tear down the connection
        client.close()







def main():

    # global variables
    global listen
    global command
    global port
    global execute
    global upload_destination
    global target

    # argument parser

    parser = argparse.ArgumentParser(description="BHP Netcat Tool")
    parser.add_argument("target_host", help="IP address of the target host")
    parser.add_argument("port", help="Target port", type=int)
    parser.add_argument('-l', '--listen', help='Listen on [host]:[port] for incoming connections', action='store_true',
                        default=False)
    parser.add_argument('-e', '--execute', help='Execute given file upon receiving a connection', type=str, default='')
    parser.add_argument('-c', '--comand', help='initialize a command shell', action='store_true', default=False)
    parser.add_argument('-u', '--upload', help='Upon receiving connection upload a file and write to [upload]', type=str,
                        default='')

    args = parser.parse_args()

    # check cli args passed in
    if args.listen:
        listen = True

    if args.commad:
        command = True

    if args.upload:
        upload_destination = args.upload

    if args.execute:
        execute = args.execute

    # are we going to listen or just send data from stdin?
    if not listen:
        # read in the buffer from the commandline
        # this will block, so send CTRL-D if not sending input to stdin
        buffer = sys.stdin.read()

    # we listen - potentiall uploads things, execute commands, drop a shell back
    if listen:
        server_loop()

if __name__ == '__main__':
    main()

