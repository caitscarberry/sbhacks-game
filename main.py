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
from gameplay.player import Player
from gameplay.events import GameEvent
from gameplay.controls import ControlsState
from networking.messaging_handler import MessagingHandler
from gameplay.physics import Simulation
import graphics.view
from gameplay.floor import Floor
import json
from queue import Queue

FRAME_LENGTH = 17


def nearby(player):
    localp = gameplay.state.players[gameplay.state.my_player_id]
    return abs(localp.roomX - player.roomX) + abs(localp.roomY - player.roomY) <= 1


def main():
    gameplay.state.curr_id = 3389
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

    running = True

    graphics.view.initView()
    gameplay.state.trapDoor = graphics.view.sprite_factory.from_file("./assets/trapdoor.png")
    gameplay.state.floor = Floor()

    if gameplay.state.my_player_id == 0:
        gameplay.state.floor.genFloor(3, 3)
        messaging.broadcast(gameplay.state.floor.serialize().encode("utf-8"))
    else:
        queue = messaging.get_messages()
        while queue.empty():
            sdl2.SDL_Delay(10)
            queue = messaging.get_messages()

        gameplay.state.floor.from_dict(json.loads(queue.get()))

    gameplay.state.players = []
    for i in range(num_players):
        new_player = Player(i, 200 + 200 * i, 350)
        gameplay.state.players.append(new_player)
        new_player.roomX = gameplay.state.floor.startingLocs[i][0]
        new_player.roomY = gameplay.state.floor.startingLocs[i][1]
        print("Starting room: %d %d" % (new_player.roomX, new_player.roomY))
        gameplay.state.floor.board[new_player.roomX][new_player.roomY].simulation.add_object(new_player.collider)


    gameplay.state.fullHeart = graphics.view.sprite_factory.from_file("./assets/hearts.png").subsprite(
        graphics.rect.Rect(0, 0, 300, 300))

    gameplay.state.emptyHeart = graphics.view.sprite_factory.from_file("./assets/hearts.png").subsprite(
        graphics.rect.Rect(600, 0, 300, 300))
    graphics.view.makeGameSubView()

    my_player = gameplay.state.players[gameplay.state.my_player_id]

    frame = 0
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

        messages = messaging.get_messages()
        while messages.qsize() > 0:
            msg = messages.get()
            game_events.append(GameEvent.deserialize(msg.decode("utf-8")))

        for event in game_events:
            if (event.params["type"] == "PLAYER"):
                gameplay.state.players[event.params["player_id"]].processPlayerEvent(event)
            if (event.params["type"] == "STATUS"):
                if (event.params["kind"] == "ROOM"):
                    gameplay.state.floor.handle_update_event(event)

        for enemy in gameplay.state.floor.board[my_player.roomX][my_player.roomY].enemies:
            enemy.chooseNewDirection(gameplay.state.players, my_player.roomX, my_player.roomY)

        nearby_ps = []
        for player in gameplay.state.players:
            if nearby(player):
                nearby_ps.append(player.id)

        monster_update = gameplay.state.floor.get_update_event(my_player.roomX, my_player.roomY)
        monster_update_str = monster_update.serialize().encode("utf-8")
        if nearby_ps[0] == gameplay.state.my_player_id and len(nearby_ps) > 1:
            if frame % 30 == 0:
                for p in nearby_ps:
                    if nearby_ps[p] != gameplay.state.my_player_id:
                        messaging.send_to(p, monster_update_str)

        curr_time = sdl2.SDL_GetTicks()
        delta = curr_time - last_phys_time
        last_phys_time = curr_time

        gameplay.state.global_queue = Queue()
        gameplay.state.floor.board[my_player.roomX][my_player.roomY].simulation.step(delta / 1000)
        while not gameplay.state.global_queue.empty():
            update_dict = gameplay.state.global_queue.get()
            messaging.broadcast(update_dict.serialize().encode("utf-8"))
            if update_dict.params["player_id"] == gameplay.state.my_player_id and \
                    update_dict.params["code"] == "CHANGE_ROOM":
                messaging.broadcast(monster_update_str)

        for player in gameplay.state.players:
            if player.id != gameplay.state.my_player_id:
                if player.roomX == my_player.roomX and player.roomY == my_player.roomY:
                    gameplay.state.floor.board[player.roomX][player.roomY].simulation.add_object(player.collider)

        graphics.view.render()

        frame_end = sdl2.SDL_GetTicks()
        remaining_time = (frame_start + FRAME_LENGTH) - frame_end
        if remaining_time > 0:
            sdl2.SDL_Delay(remaining_time)
        frame += 1

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
