from ctypes import pointer
import sdl2
import sdl2.ext
from graphics.sprite import Sprite

class Renderer:
    def __init__(self, target: sdl2.ext.Renderer, **kwargs):
        self.target = target

    def draw_sprite(self, sprite: Sprite, x, y):
        rcopy = sdl2.SDL_RenderCopy
        texture = sprite.texture
        dstrect = sdl2.SDL_Rect()
        dstrect.x = x
        dstrect.y = y
        dstrect.w = sprite.rect.width
        dstrect.h = sprite.rect.height
        sdlrender = self.target.sdlrenderer
        
        #TODO: Remove
        retcode = rcopy(sdlrender, texture, pointer(sprite.rect.rect), dstrect)
        if retcode == -1:
            raise sdl2.ext.SDLError()
