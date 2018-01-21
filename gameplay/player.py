import sdl2
from gameplay.entity import Entity
from gameplay.entity import Bullet
from gameplay.entity import Door
from gameplay.events import GameEvent
from gameplay.controls import ControlsState
from gameplay import physics
from gameplay.physics import Vec2, Polygon
from gameplay.monster import Monster
import graphics.sprite
import graphics.render
import graphics.view
import gameplay.state
import ctypes
import math

class Player(Entity):
    def __init__(self, player_id, x, y):
        self.collider = physics.PhysObject(Vec2(x, y), Polygon.square(x, y, 30, 45),
                                           self, collision_type=physics.collision_types.player)
        self.collider.add_callback(self.onDoor)
        self.collider.add_callback(self.onEnemy)
        self.MaxHealth = 500
        self.currHealth = 500
        self.width = 66
        self.height = 93
        self.speed = 200
        self.id = player_id
        self.next_bullet_id = 0
        self.sprite = None
        self.roomX = -1
        self.roomY = -1
        self.load_sprite()

    def takeDamage(self, amount):
        self.currHealth -= amount
        if self.currHealth < 0:
            print ("You Died")
            #dead
    def setRoom(self, newX, newY):
        if newX != self.roomX or newY != self.roomY:
            gameplay.state.floor.board[self.roomX][self.roomY].simulation.remove_object(self.collider)
            gameplay.state.floor.board[newX][newY].simulation.add_object(self.collider)

        self.roomX = newX
        self.roomY = newY

    def load_sprite(self):
        self.sprites = []
        for i in range(0, 4):
            self.sprite = graphics.view.sprite_factory.from_file("./assets/players.png").subsprite(
                graphics.rect.Rect(100 * i, 115 * self.id, 66, 93))
            self.sprites.append(self.sprite)

    def processInputEvent(self, event: sdl2.SDL_Event):
        # We'll want to return a GameEvent, and these fields
        # are the same regardless of what the rest of the event is
        game_event_dict = {
            "type": "PLAYER",
            "player_id": self.id,
            "pos": self.collider.pos.to_dict()
        }

        if event.type == sdl2.SDL_KEYDOWN or event.type == sdl2.SDL_KEYUP:
            state = ControlsState.state

            vel = Vec2()

            vel.x = state[sdl2.SDLK_d] - state[sdl2.SDLK_a]
            vel.y = state[sdl2.SDLK_s] - state[sdl2.SDLK_w]
            if (vel.length() > 0):
                vel = vel / vel.length()

            vel = vel * self.speed

            game_event_dict["code"] = "CHANGE_VELOCITY"
            game_event_dict["velocity"] = vel.to_dict()

            return GameEvent(game_event_dict)

        if (event.type == sdl2.SDL_MOUSEBUTTONDOWN):
            mouseX, mouseY = ctypes.c_int(0), ctypes.c_int(0) # Create two ctypes values
            # Pass x and y as references (pointers) to SDL_GetMouseState()
            buttonstate = sdl2.mouse.SDL_GetMouseState(ctypes.byref(mouseX), ctypes.byref(mouseY))
            x = mouseX.value - graphics.view.game_view.x
            y = mouseY.value - graphics.view.game_view.y
            game_event_dict["code"] = "SHOOT"
            direction_x = x - self.collider.pos.x
            direction_y = y - self.collider.pos.y
            length = math.sqrt(direction_x**2 + direction_y**2)
            direction_x = direction_x/length
            direction_y = direction_y/length
            game_event_dict["direction_x"] = direction_x
            game_event_dict["direction_y"] = direction_y
            #print(game_event_dict)
            return GameEvent(game_event_dict)

        game_event_dict["code"] = "NONE"
        return GameEvent(game_event_dict)

    def processPlayerEvent(self, event):
        if event.params["player_id"] != self.id:
            return
        self.collider.pos = Vec2.from_dict(event.params["pos"])

        if event.params["code"] == "CHANGE_VELOCITY":
            self.collider.vel = Vec2.from_dict(event.params["velocity"])

        elif event.params["code"] == "CHANGE_ROOM":
            self.collider.vel = Vec2.from_dict(event.params["velocity"])
            self.setRoom(event.params["room_x"], event.params["room_y"])

        elif (event.params["code"] == "SHOOT"):
            #each client is responsible for sending updates about its
            #player's bullets (and ONLY its player's bullets)
            #to the other clients every tick.
            #thus it is safe to have all clients execute the shoot function,
            #because the bullet's position will be quickly corrected if it gets
            #out of sync
            self.shoot(event.params["direction_x"],event.params["direction_y"])


    def shoot(self, direction_x, direction_y):
        #each bullet is identified by playerid_bulletnumber
        #this ensures that bullet ids are globally unique
        bullet = Bullet(str(self.id) + "_" + str(self.next_bullet_id), self.collider.pos.x, self.collider.pos.y, direction_x, direction_y, self.id)
        self.next_bullet_id += 1
        #print("x: %d, y: %d" % (self.roomX, self.roomY))

    def getSprite(self):
        if (self.sprite == None):
            return
        return graphics.view.SpriteToRender(self.sprites[self.directionFromVelocity()], int(self.collider.pos.x),
                                            int(self.collider.pos.y))

    def onEnemy(self, obj1, obj2):
        obj1 = obj1.owner
        obj2 = obj2.owner
        #collision with monster
        if isinstance(obj1, Player):
            foo = obj1
            obj1 = obj2
            obj2 = foo

        if not isinstance(obj1,Player) or not isinstance(obj2, Player):
            return
        if obj1.id != gameplay.state.my_player_id:
            return
        gameplay.state.players[gameplay.state.my_player_id].takeDamage(10)

    def onDoor(self, obj1, obj2):
        obj1 = obj1.owner
        obj2 = obj2.owner
        if isinstance(obj1, Door):
            foo = obj1
            obj1 = obj2
            obj2 = foo

        if not isinstance(obj1, Player) or not isinstance(obj2, Door):
            return
        if obj1.id != gameplay.state.my_player_id:
            return
        gameplay.state.players[gameplay.state.my_player_id].setRoom(obj2.toX, obj2.toY)
        # gameplay.state.floor.board[obj2.fromX][obj2.fromY].simulation.remove_object(self.collider)
        # gameplay.state.floor.board[obj2.toX][obj2.toY].simulation.add_object(self.collider)
        self.collider.pos = Vec2(500,300)

        for collider in gameplay.state.floor.board[obj2.fromX][obj2.fromY].simulation.objects:
            if isinstance(collider.owner, Player):
                gameplay.state.floor.board[obj2.fromX][obj2.fromY].simulation.remove_object(collider)

        game_event_dict = {
            "type": "PLAYER",
            "code": "CHANGE_ROOM",
            "player_id": self.id,
            "pos": self.collider.pos.to_dict(),
            "velocity": self.collider.vel.to_dict(),
            "room_x": self.roomX,
            "room_y": self.roomY
        }

        event = GameEvent(game_event_dict)
        gameplay.state.global_queue.put(event)

