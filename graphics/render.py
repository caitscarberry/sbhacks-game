from ctypes import pointer
import sdl2
import sdl2.ext
from graphics.sprite import Sprite
from gameplay.physics import Simulation

class SpriteRenderer:
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

    def draw_rect(self, x, y, w, h):
        self.target.draw_rect
        self.target.draw_rect([(int(x), int(y), int(w), int(h))])

    def draw_collision_boxes(self, sim):
        for obj in sim.objects:
            aabb = obj.aabb
            print(aabb)
            self.draw_rect(aabb.left, aabb.top, aabb.right - aabb.left, aabb.bottom - aabb.top)
