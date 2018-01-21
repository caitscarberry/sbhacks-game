from ctypes import pointer
import sdl2
import sdl2.ext
from graphics.sprite import Sprite


class SpriteRenderer:
    def __init__(self, target: sdl2.ext.Renderer, **kwargs):
        self.target = target

    def draw_sprite(self, sprite: Sprite, x, y, width=None, height=None):
        rcopy = sdl2.SDL_RenderCopy
        texture = sprite.texture
        dstrect = sdl2.SDL_Rect()

        dstrect.x = int(x - sprite.rect.width / 2)
        dstrect.y = int(y - sprite.rect.height / 2)

        if width is not None and height is not None:
            dstrect.w = width
            dstrect.h = height
        else:
            dstrect.w = sprite.rect.width
            dstrect.h = sprite.rect.height

        sdlrender = self.target.sdlrenderer
        
        #TODO: Remove
        retcode = rcopy(sdlrender, texture, pointer(sprite.rect.rect), dstrect)
        if retcode == -1:
            raise sdl2.ext.SDLError()

    def draw_rect(self, x, y, w, h):
        self.target.draw_rect
        self.target.draw_rect([(int(x) + 188, int(y), int(w), int(h))], sdl2.ext.Color(255, 0, 255))

    def draw_collision_boxes(self, sim):
        for obj in sim.objects:
            aabb = obj.aabb
            
            self.draw_rect(aabb.left, aabb.top, aabb.right - aabb.left, aabb.bottom - aabb.top)
