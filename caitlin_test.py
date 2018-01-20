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
from gameplay.entity import Player
from gameplay.events import PlayerEvent, GameEvent


class ControlsState:
    def __init__(self):
        self.state = {sdl2.SDLK_UP: False, sdl2.SDLK_DOWN: False, sdl2.SDLK_RIGHT: False, sdl2.SDLK_LEFT: False}
        self.arrow_keys = [sdl2.SDLK_UP, sdl2.SDLK_DOWN, sdl2.SDLK_RIGHT, sdl2.SDLK_LEFT]

    def should_process_input_event(self, event):
        if (event.type != sdl2.SDL_KEYDOWN and event.type != sdl2.SDL_KEYUP):
            return True
        if (not event.key.keysym.sym in self.arrow_keys):
            return False
        if ((event.type == sdl2.SDL_KEYDOWN) and (not self.state[event.key.keysym.sym])):
            return True
        if (event.type == sdl2.SDL_KEYUP):
            return True

    def update_state(self, event):
        if (event.type == sdl2.SDL_KEYDOWN):
            self.state[event.key.keysym.sym] = True
        elif (event.type == sdl2.SDL_KEYUP):
            #Reset control state when a key is released; avoids some bugs
            for key in self.arrow_keys:
                self.state[event.key.keysym.sym] = False


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
    #playersprite = graphics.sprite.Sprite.from_file("./assets/players.png")
    controls_state = ControlsState()
    while running == True:
        input_events = sdl2.ext.get_events()
        render.clear(col)
        #my_render.draw_sprite(playersprite, player.x, player.y)

        game_events = []

        for event in input_events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            else:
                if not controls_state.should_process_input_event(event):
                    continue
                player_event = players[my_player_id].processInputEvent(event)
                if player_event.code == "NONE":
                    continue
                game_events.append(player_event)
                connection.send(player_event.serialize())
                controls_state.update_state(event)

        while connection.queue.qsize() > 0:
            msg = connection.queue.get()
            game_events.append(GameEvent.deserialize(msg.decode("utf-8")))

        for event in game_events:
            if (event.type == "player"):
                players[event.player_id].processPlayerEvent(event)
        for player in players:
            player.update()
            print("%d: %d, %d" % (player.id, player.x, player.y))
        render.present()
        window.refresh()
        sdl2.SDL_Delay(16)


if __name__ == "__main__":
    main()
