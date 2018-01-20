from networking.message_queue_holder import MessageQueueHolder
from sdl2 import SDL_Delay
import sdl2
import sdl2.ext
import sdl2.ext.sprite
from sdl2.ext.color import Color
from graphics.init import init_window
import graphics.sprite
import graphics.render
import sys
import socket
from graphics.rect import Rect
from gameplay.entity import Player
from gameplay.events import GameEvent
from gameplay.controls import ControlsState
import platform
import os

WINDOW_SIZE = [1000, 650]
SIDEBAR_WIDTH = 188
GAME_WIDTH = 1000 - SIDEBAR_WIDTH

def main():
    if len(sys.argv) < 3:
        print("Please provide player file name and player id")
        sys.exit(1)

    my_player_id = None
    players_str = None
    with open(sys.argv[1], "r") as player_file:
        my_player_id = int(sys.argv[2])
        players_str = player_file.read()

    player_adds = players_str.split()
    num_players = len(player_adds)
    connections = [None] * num_players

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

        connections[p] = connection
        print("Started connection to host " + str(p))

    for p in range(num_players):
        if p == my_player_id:
            continue
        connection = connections[p]
        print("Connecting to host " + str(p) + " (" + connection.host + ":" + str(connection.port) + ")")
        while not connection.connected:
            SDL_Delay(100)

        print("Connected to host " + str(p))
        connection.start_update()

    window = init_window()
    running = True
    render = sdl2.ext.sprite.Renderer(window)
    my_render = graphics.render.Renderer(render)

    col = Color(123, 123, 123)

    spritefac = graphics.sprite.SpriteFactory(render)

    playersprite = spritefac.from_file("./assets/players.png").subsprite(graphics.rect.Rect(0, 0, 100, 100))

    players = []
    for i in range(num_players):
        players.append(Player(i, 50*i, 50))

    for player in players:
        player.load_sprite(spritefac)

    while running == True:
        input_events = sdl2.ext.get_events()

        game_events = []

        for event in input_events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            else:
                if not ControlsState.should_process_input_event(event):
                    continue
                ControlsState.update_state(event)
                player_event = players[my_player_id].processInputEvent(event)
                if player_event.params["code"] == "NONE":
                    continue
                game_events.append(player_event)
                for connection in connections:
                    if connection is None:
                        continue
                    connection.send(player_event.serialize().encode("utf-8"))

        for connection in connections:
            if connection is None:
                continue
            while connection.queue.qsize() > 0:
                msg = connection.queue.get()
                game_events.append(GameEvent.deserialize(msg.decode("utf-8")))

        for event in game_events:
            if (event.params["type"] == "PLAYER"):
                players[event.params["player_id"]].processPlayerEvent(event)
        for player in players:
            player.update()

        render.clear(col)
        for player in players:
            player.render(my_render)
        render.present()
        window.refresh()
        sdl2.SDL_Delay(16)


if __name__ == "__main__":
    main()
