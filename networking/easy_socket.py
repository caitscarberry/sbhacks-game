import socket
from threading import Thread
from time import sleep


class EasySocket:
    def __init__(self, sock=None, isServer=False):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.prefix = b''
        self.isServer = isServer
        if isServer:
            self.conn = None
            self.addr = ''

    def connect(self, host=None, port=None):
        if self.isServer:
            self.sock.bind((host, port))
            self.sock.listen(1)
            self.sock, self.addr = self.sock.accept()
        else:
            self.sock.connect((host, port))

    def send(self, msg):
        self.sock.sendall(msg)

    def receive_until(self, char=b'$'):
        ind = self.prefix.find(char)
        while ind == -1:
            chunk = self.sock.recv(1024)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            self.prefix += chunk
            ind = self.prefix.find(char)

        ret = self.prefix[0:ind]
        self.prefix = self.prefix[ind + 1:]
        return ret

"""
def threaded_function(serve):
    sock = None
    if serve:
        sock = EasySocket(sock=None, isServer=True)
        sock.connect(host="localhost", port=8080)
    else:
        sock = EasySocket(sock=None, isServer=False)
        sock.connect(host="localhost", port=8080)

    sleep(1)
    if serve:
        sock.send(b"server&")
    else:
        sock.send(b"client&")

    str = sock.receive_until(b'&')

    if serve:
        print(b"Server received: " + str)
    else:
        print(b"Client received: " + str)

if __name__ == "__main__":
    sThread = Thread(target=threaded_function, args=(True, ))
    cThread = Thread(target=threaded_function, args=(False, ))
    sThread.start()
    cThread.start()
    sThread.join()
    cThread.join()
    print("thread finished...exiting")
"""
