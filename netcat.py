#!/usr/bin/env python
# python implementation of netcat

# define some global variables
import argparse
import socket
import subprocess
import sys
import threading

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
        # connect to our target host
        client.connect((target, port))

        # check if we got any input from stdin
        # if yes, send data to tartget
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


def run_command(command):

    # trim the newline
    command = command.rstrip()

    # run the command and get the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

    except:
        output = 'Failed to execute command.\r\n'

    # send the output back to the client
    return output


def client_handler(client_socket):
    global upload_destination
    global execute
    global command

    print "New client handler"

    # check for upload
    if len(upload_destination):

        # read in all of the bytes and write to destination
        file_buffer = ''

        # read all data
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # take this data and attempt to write it out
        try:
            file_descriptor = open(upload_destination, 'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # acknowledge that the file was written
            client_socket.send("Successfully save file to {}\r\n".format(upload_destination))

        except:
            client_socket.send("Failed to save file to {}\r\n".format(upload_destination))

    # check for command execution
    if len(execute):

        # run command
        output = run_command(execute)

        client_socket.send(output)

    # go into loop if command shell was requested
    if command:

        while True:
            # show a simple prompt
            client_socket.send("<BHP:#> ")

            # recv until linefeed is received (return key pressed)
            cmd_buffer = ""
            while '\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # send back command output
            response = run_command(cmd_buffer)

            #send back the response
            client_socket.send(response)


def server_loop():
    global target

    # if no target is defined, listen on all interfaces
    if not len(target):
        target = '0.0.0.0'

    print '[*] Listening on {}:{}'.format(target, port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)

    while True:
        # when server receives a connection - have a client socket and remote addr and port
        client_socket, addr = server.accept()
        print '[*] Received connection from {}:{}'.format(addr[0], addr[1])

        # create a thread for each client that connects to server
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


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
    parser.add_argument('-t', "--target", help="IP address of the target host", type=str, default='')
    parser.add_argument('-p', "--port", help="Target port", type=int, default=0)
    parser.add_argument('-l', '--listen', help='Listen on [host]:[port] for incoming connections', action='store_true',
                        default=False)
    parser.add_argument('-e', '--execute', help='Execute given file upon receiving a connection', type=str, default='')
    parser.add_argument('-c', '--command', help='initialize a command shell', action='store_true', default=False)
    parser.add_argument('-u', '--upload', help='Upon receiving connection upload a file and write to [upload]', type=str,
                        default='')

    args = parser.parse_args()

    # check cli args passed in
    if args.target:
        target = args.target

    if args.port:
        port = args.port

    if args.listen:
        listen = True

    if args.command:
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

        # send data off
        client_sender(buffer)

    # we listen - potentially uploads things, execute commands, drop a shell back
    if listen:

        server_loop()

if __name__ == '__main__':
    main()

