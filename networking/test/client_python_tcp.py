#!/usr/bin/env python

#tcp code structure borrowed from : https://wiki.python.org/moin/TcpCommunication 

import socket
import sys

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024

#connect to sockets and get input 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
message = raw_input("Enter string: ")
s.send(message)

#receive data back from server
while 1:
    data = s.recv(BUFFER_SIZE)
    if data == 'Error':
        print "Sorry, cannot compute!"
    else:
        if not data: break #break when there is no more data
        for val in data.split():
            print "From server:", val
s.close()

