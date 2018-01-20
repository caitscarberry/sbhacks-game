import sdl2
from gameplay import physics
from gameplay.events import GameEvent
from gameplay.controls import ControlsState
from graphics.rect import Rect
import graphics.sprite
import graphics.render


class Entity:
    def __init__(self, pos=physics.Vec2(), sprite=None):
        self.pos = pos
        self.sprite = sprite
     
    def processInputEvent(self):
        pass
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    #directions in sprite sheet order
    #front right back left
    #  0     1     2    3
    def directionFromVelocity(self):
        if (self.velocity_x > 0):
            return 1
        if (self.velocity_x < 0):
            return 3
        if (self.velocity_y < 0):
            return 2
        return 0

    def render(self, renderer):
        pass


class Player(Entity):
    def __init__(self, player_id, x, y):
        self.velocity_x = 0
        self.velocity_y = 0
        self.x = x
        self.y = y
        self.speed = 1
        self.id = player_id
        self.next_bullet_id = 0
        self.sprite = None
        self.width = 66
        self.height = 93
        self.roomX = -1
        self.roomY = -1

    def setRoom(self, x, y):
        self.roomX = x
        self.roomY = y

    def load_sprite(self, spritefac):
        self.sprites = []
        for i in range(0,4):
            self.sprite = spritefac.from_file("./assets/players.png").subsprite(graphics.rect.Rect(100*i, 115*self.id, 66, 93))
            self.sprites.append(self.sprite)

    def processInputEvent(self, event: sdl2.SDL_Event):
        #We'll want to return a GameEvent, and these fields
        #are the same regardless of what the rest of the event is
        game_event_dict = {
            "type": "PLAYER",
            "player_id": self.id,
            "x": self.x,
            "y": self.y,
        }

        if event.type == sdl2.SDL_KEYDOWN or event.type == sdl2.SDL_KEYUP:
            state = ControlsState.state
            velocity_x = state[sdl2.SDLK_RIGHT] - state[sdl2.SDLK_LEFT]
            velocity_y = state[sdl2.SDLK_DOWN] - state[sdl2.SDLK_UP]

            game_event_dict["code"] = "CHANGE_VELOCITY"
            game_event_dict["velocity_x"] = velocity_x
            game_event_dict["velocity_y"] = velocity_y

            return GameEvent(game_event_dict)

        game_event_dict["code"] = "NONE"
        return GameEvent(game_event_dict)

    def processPlayerEvent(self, event):
        if (event.params["player_id"] != self.id):
            return
        self.x = int(event.params["x"])
        self.y = int(event.params["y"])
        if (event.params["code"] == "CHANGE_VELOCITY"):
            self.velocity_x = int(event.params["velocity_x"])
            self.velocity_y = int(event.params["velocity_y"])
        elif (event.params["code"] == "SHOOT"):
            #each client is responsible for sending updates about its
            #player's bullets (and ONLY its player's bullets)
            #to the other clients every tick.
            #thus it is safe to have all clients execute the shoot function,
            #because the bullet's position will be quickly corrected if it gets
            #out of sync
            self.shoot(event.direction)

    def shoot(self, direction):
        #each bullet is identified by playerid_bulletnumber
        #this ensures that bullet ids are globally unique
        bullet = Bullet(self.id + "_" + self.next_bullet_id, x, y, direction, self.id)
        self.next_bullet_id += 1

    def render(self, renderer):
        if (self.sprite == None):
            return
        renderer.draw_sprite(self.sprites[self.directionFromVelocity()], int(self.x), int(self.y))

class Bullet(Entity):
    def __init__ (self, bullet_id, x, y, direction, player_id):
        self.id = bullet_id
        self.x = x
        self.y = y
        self.speed = 5
        self.x_velocity = self.speed * math.cos(direction)
        self.y_velocity = self.speed * math.sin(direction)
        #the player that fired this bullet
        self.player_id = player_id
