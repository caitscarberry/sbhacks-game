from networking.message_queue_holder import MessageQueueHolder
from sdl2 import SDL_Delay

s = MessageQueueHolder(True)
c = MessageQueueHolder(False)

s.start_connect("localhost", 8080)
c.start_connect("localhost", 8080)

while not s.connected or not c.connected:
    if c.connected:
        print("Client is connected")
    else:
        print("Client is not connected")

    if s.connected:
        print("Server is connected")
    else:
        print("Server is not connected")

if c.connected:
    print("Client is connected")
else:
    print("Client is not connected")

if s.connected:
    print("Server is connected")
else:
    print("Server is not connected")

s.start_update()
c.start_update()

s.send(b"test1")
s.send(b"test2")
SDL_Delay(500)
print("Server queue size: " + str(s.queue.qsize()))
print("Client queue size: " + str(c.queue.qsize()))
c.queue.get()
c.queue.get()

c.send(b"test1")
c.send(b"test2")
s.send(b"test2")
SDL_Delay(500)
print("Server queue size: " + str(s.queue.qsize()))
print("Client queue size: " + str(c.queue.qsize()))
