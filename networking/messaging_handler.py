from networking.message_queue_holder import MessageQueueHolder
from sdl2 import SDL_Delay
from queue import Queue

class MessagingHandler:
    def __init__(self):
        self.connections = None

    def connect(self, player_adds, num_players, my_player_id):
        self.connections = [None] * num_players
        for p in range(num_players):
            if p == my_player_id:
                continue
            connection = None
            iAmServer = p > my_player_id
            if iAmServer:
                connection = MessageQueueHolder(True)
                connection.start_connect(player_adds[my_player_id], 25565 + p)
            else:
                connection = MessageQueueHolder(False)
                connection.start_connect(player_adds[p], 25565 + my_player_id)

            self.connections[p] = connection
            print("Started connection to host " + str(p))

        for p in range(num_players):
            if p == my_player_id:
                continue
            connection = self.connections[p]
            print("Connecting to host " + str(p) + " (" + connection.host + ":" + str(connection.port) + ")")
            while not connection.connected:
                SDL_Delay(100)

            print("Connected to host " + str(p))
            connection.start_update()

        print("Finished connecting")

    def get_messages(self):
        ret = Queue()
        for connection in self.connections:
            if connection is None:
                continue
            while not connection.queue.empty():
                ret.put(connection.queue.get())
        return ret
