import sdl2
import sdl2.ext
import ctypes
from graphics.render import SpriteRenderer
from graphics.sprite import SpriteFactory
from gameplay.room import Room
import gameplay.state
import collections

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
    global subviews
    subviews = []

def makeGameSubView():
    subviews.append(GameView(SIDEBAR_WIDTH,0,GAME_WIDTH,WINDOW_SIZE[1]))

def render():
    raw_renderer.clear((0,0,0))
    for subview in subviews:
        subview.render()
    raw_renderer.present()
    window.refresh()

SpriteToRender = collections.namedtuple('SpriteToRender',('img','x','y'))

class SubView:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def renderSprite(self,sprite, x, y):
        sprite_renderer.draw_sprite(sprite, x + self.x, y + self.y)

    """def renderSpriteCentered(sprite, x, y):
        sprite_renderer.draw_sprite(sprite, x + self.x, y + self.y)"""

class GameView(SubView):
    def __init__(self, x, y, height, width):
        super().__init__(x, y, height, width)

    def render(self):
        sprites = Room().getSprites()
        for sprite in sprites:
            self.renderSprite(sprite.img, sprite.x, sprite.y)
        for player in gameplay.state.players:
            sprite = player.getSprite()
            self.renderSprite(sprite.img, sprite.x, sprite.y)
        #TODO: render cursor