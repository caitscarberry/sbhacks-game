#!/usr/bin/env python

#tcp code structure borrowed from : https://wiki.python.org/moin/TcpCommunication 
import socket
import sys

TCP_IP = socket.gethostbyname (socket.gethostname())
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024 

#bind socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()

#recieve request from client
data = conn.recv(BUFFER_SIZE)

#compute result and send it back to client
try:
    inputNum = int(data)
    if (inputNum > 9):
        while (inputNum > 9):
            sumDigits = 0
            while (inputNum > 9):
                sumDigits = sumDigits + inputNum % 10;
                inputNum = inputNum / 10
            sumDigits = sumDigits + inputNum
            inputNum = sumDigits
            conn.send(str(sumDigits) + " ")
    else:
        conn.send(str(inputNum))
    
except ValueError:
    conn.send("Error")

conn.close()
