import socket


class EasySocket:
    def __init__(self, isServer=False):
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.prefix = b''
        self.isServer = isServer
        if isServer:
            self.conn = None
            self.addr = ''

    def connect(self, host, port):
        if self.isServer:
            self.sock.bind((host, port))
            self.sock.listen(1)
            self.sock, self.addr = self.sock.accept()
        else:
            connected = False
            while not connected:
                try:
                    self.sock.connect((host, port))
                    connected = True
                except Exception:
                    print("Connection to " + host + " failed, retrying")


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
