from networking.easy_socket import EasySocket
from gameplay.flood import connected
import json

room = [[0] * 10 for _ in range(10)]
room[9][3] = 1
room[9][4] = 1
room[9][5] = 1

print(connected(room))
