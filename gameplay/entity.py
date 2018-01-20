from gameplay import physics

class Entity:
    def __init__(self, pos=physics.Vec2()):
        self.pos = pos
     
    def processInputEvt(self):
        pass
    
    def update(self):
        pass
    

class Player(Entity):
    def __init__(self, x, y):
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 1

    def processInputEvt(self):
        gameEvts = []
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_UP:
                self.velocity_y = -self.speed
            elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                self.velocity_y = self.speed
            elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                self.velocity_x = self.speed
            elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                self.velocity_x = -self.speed
        elif event.type == sdl2.SDL_KEYUP:
            if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN, sdl2.SDLK_RIGHT, sdl2.SDLK_LEFT):
                self.velocity_x = 0
                self.velocity_y = 0
