import sdl2
from gameplay import physics
from gameplay.physics import Vec2, Polygon
from gameplay.events import GameEvent
from gameplay.controls import ControlsState
from graphics.rect import Rect
import graphics.sprite
import graphics.render
import graphics.view


class Entity:
    def __init__(self, collider: physics.PhysObject, sprite=None):
        self.collider = collider
        self.sprite = sprite
     
    def processInputEvent(self):
        pass
    
    def update(self):
        pass

    #directions in sprite sheet order
    #front right back left
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


class Player(Entity):
    def __init__(self, player_id, x, y):
        self.collider = physics.PhysObject(Vec2(x, y), Polygon.square(x, y, 66, 93))
        self.width = 66
        self.height = 93
        self.speed = 100
        self.id = player_id
        self.next_bullet_id = 0
        self.sprite = None
        self.roomX = -1
        self.roomY = -1
        self.x = x
        self.y = y

        self.load_sprite()

    def setRoom(self, x, y):
        self.roomX = x
        self.roomY = y

    def load_sprite(self):
        self.sprites = []
        for i in range(0,4):
            self.sprite = graphics.view.sprite_factory.from_file("./assets/players.png").subsprite(graphics.rect.Rect(100*i, 115*self.id, 66, 93))
            self.sprites.append(self.sprite)

    def processInputEvent(self, event: sdl2.SDL_Event):
        #We'll want to return a GameEvent, and these fields
        #are the same regardless of what the rest of the event is
        game_event_dict = {
            "type": "PLAYER",
            "player_id": self.id,
            "pos": self.collider.pos.to_dict()
        }

        if event.type == sdl2.SDL_KEYDOWN or event.type == sdl2.SDL_KEYUP:
            state = ControlsState.state
            
            self.collider.vel.x = self.speed * (state[sdl2.SDLK_RIGHT] - state[sdl2.SDLK_LEFT])
            self.collider.vel.y = self.speed * (state[sdl2.SDLK_DOWN] - state[sdl2.SDLK_UP])

            game_event_dict["code"] = "CHANGE_VELOCITY"
            game_event_dict["velocity"] = self.collider.vel.to_dict()

            return GameEvent(game_event_dict)

        game_event_dict["code"] = "NONE"
        return GameEvent(game_event_dict)

    def processPlayerEvent(self, event):
        if (event.params["player_id"] != self.id):
            return
        self.collider.pos.from_dict(event.params["pos"])
        
        if (event.params["code"] == "CHANGE_VELOCITY"):
            self.collider.vel.from_dict(event.params["velocity"])
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

    def getSprite(self):
        if (self.sprite == None):
            return

        return graphics.view.SpriteToRender(self.sprites[self.directionFromVelocity()], int(self.x), int(self.y))

class Bullet(Entity):
    def __init__ (self, bullet_id, x, y, direction, player_id):
        self.id = bullet_id
        self.speed = 5
        #the player that fired this bullet
        self.player_id = player_id
