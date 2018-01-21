import sdl2
from gameplay import physics
from gameplay.physics import Vec2, Polygon
from gameplay.events import GameEvent
from gameplay.controls import ControlsState
from graphics.rect import Rect
import graphics.sprite
import graphics.render
import graphics.view
import gameplay.state
import ctypes
import math

class Entity:
    def __init__(self, collider: physics.PhysObject, sprite=None):
        self.collider = collider
        self.sprite = sprite

    def processInputEvent(self):
        pass

    def update(self):
        pass

    # directions in sprite sheet order
    # front right back left
    #  0     1     2    3
    def directionFromVelocity(self):
        if (self.collider.vel.x > 0):
            return 1
        if (self.collider.vel.x < 0):
            return 3
        if (self.collider.vel.y < 0):
            return 2
        return 0

    def render(self, renderer):
        pass

class Door(Entity):
    def __init__(self, dir, nextX, nextY, pastX, pastY):
        self.toX = nextX
        self.toY = nextY
        self.fromX = pastX
        self.fromY = pastY
        leftX = 32
        midX = graphics.view.GAME_WIDTH / 2
        rightX = graphics.view.GAME_WIDTH - 32
        topY = 32
        midY = graphics.view.WINDOW_SIZE[1] / 2
        botY = graphics.view.WINDOW_SIZE[1] - 32
        if dir == 0:
            self.collider = physics.PhysObject(Vec2(midX, topY),
                                               Polygon.square(midX, topY, 64, 64), self,
                                               collision_type=physics.collision_types.trigger)
        elif dir == 1:
            self.collider = physics.PhysObject(Vec2(rightX, midY),
                                               Polygon.square(rightX, midY, 64, 64), self,
                                               collision_type=physics.collision_types.trigger)
        elif dir == 2:
            self.collider = physics.PhysObject(Vec2(midX, botY),
                                               Polygon.square(midX, botY, 64, 64), self,
                                               collision_type=physics.collision_types.trigger)
        elif dir == 3:
            self.collider = physics.PhysObject(Vec2(leftX, midY),
                                               Polygon.square(leftX, midY, 64, 64), self,
                                               collision_type=physics.collision_types.trigger)
        self.speed = 0
        self.width = 64
        self.height = 64
        self.sprite = None
        self.loadSprite(dir)

    def loadSprite(self, dir):
        if dir == 0:
            self.sprite = gameplay.state.doorT
        elif dir == 1:
            self.sprite = gameplay.state.doorR
        elif dir == 2:
            self.sprite = gameplay.state.doorB
        elif dir == 3:
            self.sprite = gameplay.state.doorL

    def getSprite(self):
        if (self.sprite == None):
            return
        return graphics.view.SpriteToRender(self.sprite, int(self.collider.pos.x),
                                            int(self.collider.pos.y), 64, 64)


class Player(Entity):
    def __init__(self, player_id, x, y):
        self.collider = physics.PhysObject(Vec2(x, y), Polygon.square(x, y, 30, 45),
                                           self, collision_type=physics.collision_types.player)
        self.collider.add_callback(self.onDoor)
        self.width = 66
        self.height = 93
        self.speed = 200
        self.id = player_id
        self.next_bullet_id = 0
        self.sprite = None
        self.roomX = -1
        self.roomY = -1
        self.load_sprite()

    def setRoom(self, x, y):
        self.roomX = x
        self.roomY = y

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

            vel.x = state[sdl2.SDLK_RIGHT] - state[sdl2.SDLK_LEFT]
            vel.y = state[sdl2.SDLK_DOWN] - state[sdl2.SDLK_UP]
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
        self.collider.pos.from_dict(event.params["pos"])

        if event.params["code"] == "CHANGE_VELOCITY":
            self.collider.vel.from_dict(event.params["velocity"])

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

    def onDoor(self, obj1, obj2):
        print("here")
        obj1 = obj1.owner
        obj2 = obj2.owner
        if isinstance(obj1, Door):
            gameplay.state.players[gameplay.state.my_player_id].roomX = obj1.toX
            gameplay.state.players[gameplay.state.my_player_id].roomY = obj1.toY
            gameplay.state.floor.board[obj1.fromX][obj1.fromY].simulation.remove_object(self.collider)
            gameplay.state.floor.board[obj1.toX][obj1.toY].simulation.add_object(self.collider)
            self.collider.pos = Vec2()
        elif isinstance(obj2, Door):
            gameplay.state.players[gameplay.state.my_player_id].roomX = obj2.toX
            gameplay.state.players[gameplay.state.my_player_id].roomY = obj2.toY
            gameplay.state.floor.board[obj2.fromX][obj2.fromY].simulation.remove_object(self.collider)
            gameplay.state.floor.board[obj2.toX][obj2.toY].simulation.add_object(self.collider)


class Bullet(Entity):
    def __init__ (self, bullet_id, x, y, direction_x, direction_y, player_id):
        print("shooting")
        self.id = bullet_id
        self.speed = 80
        #the player that fired this bullet
        self.player_id = player_id
        self.collider = physics.PhysObject(Vec2(x+direction_x*5, y+direction_y*5), Polygon.square(x+direction_x*5, y+direction_y*5, 10, 10), self, collision_type=physics.collision_types.player)
        self.collider.add_callback(self.onCollide)
        roomx = gameplay.state.players[player_id].roomX
        roomy = gameplay.state.players[player_id].roomY
        room = gameplay.state.floor.board[roomx][roomy]
        room.simulation.add_object(self.collider)
        room.projectiles[self.id] = self
        if player_id == gameplay.state.my_player_id:
            gameplay.state.responsible_for.append(self.id)
        self.collider.vel.x = direction_x * self.speed
        self.collider.vel.y = direction_y * self.speed
        self.load_sprite()
        self.alive = True

    def load_sprite(self):
        self.sprite = graphics.view.sprite_factory.from_file("./assets/players.png").subsprite(graphics.rect.Rect(100, 115, 66, 93))

    def getSprite(self):
        if (self.sprite == None):
            return
        return graphics.view.SpriteToRender(self.sprite, int(self.collider.pos.x), int(self.collider.pos.y))

    def onCollide(self, collider: physics.PhysObject, other: physics.PhysObject):
        if collider.collision_type == physics.collision_types.static or \
           collider.collision_type == physics.collision_types.dynamic or \
           other.collision_type == physics.collision_types.static or \
           other.collision_type == physics.collision_types.dynamic:
            self.alive = False
