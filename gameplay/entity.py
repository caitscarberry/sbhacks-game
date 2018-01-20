import sdl2
from gameplay import physics

class Entity:
    def __init__(self, pos=physics.Vec2()):
        self.pos = pos
     
    def processInputEvt(self):
        pass
    
    def update(self):
        pass
    

class PlayerEvt:
    def __init__(player_id, x, y, evt_type):
        self.player_id = player_id
        self.x = x
        self.y = y
        self.type = evt_type

class Player(Entity):
    def __init__(self, player_id, x, y):
        self.velocity_x = 0
        self.velocity_y = 0
        self.x = x
        self.y = y
        self.speed = 1
        self.id = player_id
        self.next_bullet_id = 0

    def processInputEvt(self, event: sdl2.SDL_Event):
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_UP:
                return PlayerEvt(self.id, self.x, self.y, "START_MOVING_UP")
            elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                return PlayerEvt(self.id, self.x, self.y, "START_MOVING_DOWN")
            elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                return PlayerEvt(self.id, self.x, self.y, "START_MOVING_RIGHT")
            elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                return PlayerEvt(self.id, self.x, self.y, "START_MOVING_LEFT")

        elif event.type == sdl2.SDL_KEYUP:
            if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                return PlayerEvt(self.id, self.x, self.y, "STOP_MOVING_Y")
            if event.key.keysym.sym in (sdl2.SDLK_RIGHT, sdl2.SDLK_LEFT):
                return PlayerEvt(self.id, self.x, self.y, "STOP_MOVING_X")

    def processPlayerEvt(self, evt):
        if (evt.player_id != this.id):
            return
        self.x = evt.x
        self.y = evt.y
        if (evt.type == "START_MOVING_LEFT"):
            self.velocity_x = self.speed
        if (evt.type == "START_MOVING_RGHT"):
            self.velocity_x = self.speed
        if (evt.type == "START_MOVING_UP"):
            self.velocity_y = -self.speed
        if (evt.type == "START_MOVING_DOWN"):
            self.velocity_y = self.speed
        if (evt.type == "STOP_MOVING_Y"):
            self.velocity_y = 0
        if (evt.type == "STOP_MOVING_X"):
            self.velocity_x = 0
        if (evt.type == "SHOOT"):
            #each client is responsible for sending updates about its
            #player's bullets (and ONLY its player's bullets)
            #to the other clients every tick.
            #thus it is safe to have all clients execute the shoot function,
            #because the bullet's position will be quickly corrected if it gets
            #out of sync
            self.shoot(evt.direction)

    def shoot(self, direction):
        #each bullet is identified by playerid_bulletnumber
        #this ensures that bullet ids are globally unique
        bullet = Bullet(self.id + "_" + self.next_bullet_id, x, y, direction, self.id)
        self.next_bullet_id += 1


class Bullet(Entity):
    def __init__ (bullet_id, x, y, direction, player_id):
        self.id = bullet_id
        self.x = x
        self.y = y
        self.speed = 5
        self.x_velocity = self.speed * math.cos(direction)
        self.y_velocity = self.speed * math.sin(direction)
        #the player that fired this bullet
        self.player_id = player_id
