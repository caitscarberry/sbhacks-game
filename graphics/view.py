import sdl2
import sdl2.ext
import ctypes
from graphics.render import SpriteRenderer
from graphics.sprite import SpriteFactory


WINDOW_SIZE = [1000, 650]
SIDEBAR_WIDTH = 188
GAME_WIDTH = 1000 - SIDEBAR_WIDTH

def initWindow():
    sdl2.ext.init()
    global window
    window = sdl2.ext.Window("Hackathon", WINDOW_SIZE)
    window.show()

def initRenderers():
	global raw_renderer
	raw_renderer = sdl2.ext.sprite.Renderer(window)
	global sprite_renderer
	sprite_renderer = SpriteRenderer(raw_renderer)
	global sprite_factory
	sprite_factory = SpriteFactory(raw_renderer)

def initView():
	initWindow()
	initRenderers()


class SubView:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def render(sprite, x, y):
    	sprite_renderer.draw_sprite(sprite, x + self.x, y + self.y)