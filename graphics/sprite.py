import sdl2

class Sprite:
    def __init__(self, texture: sdl2.SDL_Surface, width=0, height=0):
        self.texture = texture
        self.width = texture.w
        self.height = texture.h

    @classmethod
    def from_file(self, filename: str):
        surface = sdl2.ext.load_image(filename)
        return Sprite(surface)
