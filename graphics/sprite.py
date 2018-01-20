import sdl2
import sdl2.ext
import ctypes

from graphics.rect import Rect

class Sprite:
    def __init__(self, texture: sdl2.SDL_Texture, rect):
        self.texture = texture
        self.rect = rect

    def subsprite(self, subrect:Rect):
        if not self.rect.contains(subrect):
            raise ValueError("Subsprite must be within sprite bounds")

        subrect.x += self.rect.x
        subrect.y += self.rect.y
        return Sprite(self.texture, subrect)
            


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
        rect = Rect(0, 0, w, h)
        return Sprite(texture, rect)
