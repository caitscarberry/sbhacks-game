from networking.easy_socket import EasySocket
from threading import Thread
from queue import Queue

class MessageQueueHolder:
    def __init__(self, isServer):
        self.queue = Queue()
        self.socket = EasySocket(isServer)
        self.connected = False
        self.host = None
        self.port = None

    def _connect(self, host, port):
        self.host = host
        self.port = port
        self.socket.connect(host, port)
        self.connected = True

    def start_connect(self, host, port):
        sThread = Thread(target=self._connect, args=(host, port,))
        sThread.start()

    def _update_queue(self):
        while True:
            self.queue.put(self.socket.receive_until())

    def start_update(self):
        sThread = Thread(target=self._update_queue, args=())
        sThread.start()

    def send(self, msg):
        self.socket.send(msg + b"$")
