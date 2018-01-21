from networking.message_queue_holder import MessageQueueHolder
from sdl2 import SDL_Delay
from sdl2 import SDL_GetTicks
import gameplay.state
import graphics.view
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
from networking.messaging_handler import MessagingHandler
from gameplay.physics import Simulation
import graphics.view
from gameplay.floor import Floor
from gameplay.monster import Monster
from gameplay.room import Room

FRAME_LENGTH = 17


def main():
    if len(sys.argv) < 3:
        print("Please provide player file name and player id")
        sys.exit(1)

    gameplay.state.my_player_id = None
    players_str = None
    with open(sys.argv[1], "r") as player_file:
        gameplay.state.my_player_id = int(sys.argv[2])
        players_str = player_file.read()

    player_adds = players_str.split()
    num_players = len(player_adds)

    messaging = MessagingHandler()
    messaging.connect(player_adds, num_players, gameplay.state.my_player_id)

    graphics.view.initView()
    graphics.view.makeGameSubView()
    running = True

    gameplay.state.floor = Floor()
    gameplay.state.floor.genFloor(10, 25)
    gameplay.state.players = []
    sim = Simulation()

    for i in range(num_players):
        gameplay.state.players.append(Player(i, 50 * i, 50))
        sim.add_object(gameplay.state.players[i].collider)

    gameplay.state.floor.board[0][0] = Room()
    gameplay.state.floor.board[0][0].enemies = []
    gameplay.state.floor.board[0][0].enemies.append(Monster(0, 100, 100))
    sim.add_object(gameplay.state.floor.board[0][0].enemies[0].collider)

    last_phys_time = sdl2.SDL_GetTicks()
    while running == True:
        frame_start = sdl2.SDL_GetTicks()

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
                player_event = gameplay.state.players[gameplay.state.my_player_id].processInputEvent(event)
                if player_event.params["code"] == "NONE":
                    continue
                game_events.append(player_event)
                messaging.broadcast(player_event.serialize().encode("utf-8"))

        for enemy in gameplay.state.floor.board[0][0].enemies:
            enemy.chooseNewDirection(gameplay.state.players)

        messages = messaging.get_messages()
        while messages.qsize() > 0:
            msg = messages.get()
            game_events.append(GameEvent.deserialize(msg.decode("utf-8")))

        for event in game_events:
            if (event.params["type"] == "PLAYER"):
                gameplay.state.players[event.params["player_id"]].processPlayerEvent(event)

        curr_time = sdl2.SDL_GetTicks()
        delta = curr_time - last_phys_time
        last_phys_time = curr_time
        sim.step(delta / 1000)

        graphics.view.render()

        frame_end = sdl2.SDL_GetTicks()
        remaining_time = (frame_start + FRAME_LENGTH) - frame_end
        if remaining_time > 0:
            sdl2.SDL_Delay(remaining_time)

    sdl2.ext.quit()


if __name__ == "__main__":
    try:
        main()
    except sdl2.ext.SDLError:
        pass
    except RuntimeError as e:
        print(e)
    finally:
        sdl2.ext.quit()



