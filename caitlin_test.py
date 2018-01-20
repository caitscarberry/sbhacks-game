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

def main():
    window = init_window()
    running = True
    render = sdl2.ext.sprite.Renderer(window)
    my_render = graphics.render.Renderer(render)

    connection = None
    me = input()
    iAmServer = me.startswith("s")
    players = [Player(0, 0, 0), Player(1, 200, 200)]
    my_player_id = None
    if iAmServer:
        my_player_id = 0
        print("Server")
        connection = MessageQueueHolder(True)
        #changed this back for local testing, will not
        #work across machines
        connection.start_connect("localhost", 8080)
    else:
        my_player_id = 1
        print("Client")
        connection = MessageQueueHolder(False)
        connection.start_connect("localhost", 8080)

    print("Connecting")
    while not connection.connected:
        SDL_Delay(100)

    print("Connected")
    connection.start_update()

    col = Color(123, 123, 123)

    spritefac = graphics.sprite.SpriteFactory(render)
    playersprite = spritefac.from_file("./assets/players.png").subsprite(graphics.rect.Rect(0, 0, 100, 100))

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
                connection.send(player_event.serialize().encode("utf-8"))

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
            my_render.draw_sprite(playersprite, int(player.x), int(player.y))
        render.present()
        window.refresh()
        sdl2.SDL_Delay(16)


if __name__ == "__main__":
    main()
