from ctypes import pointer
import sdl2
import sdl2.ext
from graphics.sprite import Sprite

class Renderer:
    def __init__(self, target: sdl2.ext.Renderer, **kwargs):
        self.target = target

    def draw_sprite(self, sprite: Sprite, x, y):
        rect = sdl2.SDL_Rect()
        rcopy = sdl2.SDL_RenderCopy
        texture = sprite.texture
        
        rect.w, rect.h = sprite.width, sprite.height
        rect.x = x
        rect.y = y
        sdlrender = self.target.sdlrenderer
        print(type(sdlrender))
        #TODO: Remove
        texture = sdl2.SDL_CreateTextureFromSurface(sdlrender.contents, texture)
        retcode = rcopy(sdlrender, texture, None, pointer(rect))
        if retcode == -1:
            raise sdl2.ext.SDLError()
