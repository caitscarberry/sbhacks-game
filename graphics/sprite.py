import sdl2
import sdl2.ext
import ctypes

class Sprite:
    def __init__(self, texture: sdl2.SDL_Texture, width=0, height=0):
        self.texture = texture
        self.width = width
        self.height = height


# I HATE IT
class SpriteFactory:
    def __init__(self, render:sdl2.ext.Renderer):
        self.render = render
        self.sdlrender = render.sdlrenderer

    def extract_texture(self, surface:sdl2.SDL_Surface):
        return sdl2.SDL_CreateTextureFromSurface(self.sdlrender, ctypes.pointer(surface))


    def from_file(self, filename: str):
        surface = sdl2.ext.load_image(filename)
        w, h = surface.w, surface.h
        texture = self.extract_texture(surface)
        return Sprite(texture, w, h)
