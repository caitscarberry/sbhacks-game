from networking.message_queue_holder import MessageQueueHolder
from sdl2 import SDL_Delay
import sdl2
import sdl2.ext
import sdl2.ext.sprite
from sdl2.ext.color import Color
import graphics.sprite
import graphics.render
import sys
import socket

from graphics.rect import Rect
from gameplay.entity import Player
from gameplay.events import GameEvent
from gameplay.controls import ControlsState
from gameplay import physics
from networking.messaging_handler import MessagingHandler
import graphics.view

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

    messaging = MessagingHandler()
    messaging.connect(player_adds, num_players, my_player_id)

    graphics.view.initView()

    running = True

    col = Color(123, 123, 123)

    players = []
    for i in range(num_players): 
        players.append(Player(i, 50*i, 50))

            
    sim = physics.Simulation()
    dg = graphics.view.sprite_factory.from_file("./assets/dungeon.png")
    r = dg.rect
    wall = physics.PhysObject(physics.Vec2(300, 300), physics.Polygon.square(300, 300, 200, 200))
    player = players[0]
    sim.add_object(player.collider)
    player.collider.collision_type = physics.PhysObject.collision_types.dynamic
    sim.add_object(wall)
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
                messaging.broadcast(player_event.serialize().encode("utf-8"))
        messages = messaging.get_messages()
        while messages.qsize() > 0:
            msg = messages.get()
            game_events.append(GameEvent.deserialize(msg.decode("utf-8")))

        for event in game_events:
            if (event.params["type"] == "PLAYER"):
                players[event.params["player_id"]].processPlayerEvent(event)
        #for player in players:
        #    player.update()
        sim.step(16 / 1000)
        graphics.view.raw_renderer.clear(col)
        #graphics.view.sprite_renderer.draw_sprite(dg, wall.pos.x, wall.pos.y)
        for player in players:
            player.render(graphics.view.sprite_renderer)

        graphics.view.sprite_renderer.draw_collision_boxes(sim)
        graphics.view.raw_renderer.present()
        graphics.view.window.refresh()
        sdl2.SDL_Delay(16)


if __name__ == "__main__":
    main()
