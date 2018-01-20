import sdl2

class Sprite:
    def __init__(self, texture: sdl2.SDL_Surface):
        self.texture = texture
