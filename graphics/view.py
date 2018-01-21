import sdl2
import sdl2.ext
import ctypes
from graphics.render import SpriteRenderer
from graphics.sprite import SpriteFactory
import gameplay.state
from graphics.sprite_to_render import SpriteToRender

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
    global game_view
    game_view = GameView(SIDEBAR_WIDTH,0,GAME_WIDTH,WINDOW_SIZE[1])
    subviews.append(game_view)

def render():
    raw_renderer.clear((0,0,0))
    for subview in subviews:
        subview.render()
    raw_renderer.present()
    window.refresh()

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
        roomX = gameplay.state.players[gameplay.state.my_player_id].roomX
        roomY = gameplay.state.players[gameplay.state.my_player_id].roomY
        sprites = gameplay.state.floor.board[roomX][roomY].getSprites()
        if (sprites is None):
            return
        for sprite in sprites:
            self.renderSprite(sprite.img, sprite.x, sprite.y)
        for player in gameplay.state.players:
            sprite = player.getSprite()
            self.renderSprite(sprite.img, sprite.x, sprite.y)

        #Renders current room enemies
        for enemy in gameplay.state.floor.board[roomX][roomY].enemies:
            if not isinstance(enemy, int):
                sprite = enemy.getSprite()
                self.renderSprite(sprite.img, sprite.x, sprite.y)
