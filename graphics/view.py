import sdl2
import sdl2.ext
import ctypes
from graphics.render import Renderer

WINDOW_SIZE = [1000, 650]
SIDEBAR_WIDTH = 188
GAME_WIDTH = 1000 - SIDEBAR_WIDTH

def initWindow():
    sdl2.ext.init()
    global window
    window = sdl2.ext.Window("Hackathon", WINDOW_SIZE)
    window.show()
    return window

def initRenderers():
	global raw_renderer
	raw_renderer = sdl2.ext.sprite.Renderer(window)
	global sprite_renderer
	sprite_renderer = Renderer(raw_renderer)



class SubView():
    def __init__(self):
        pass

class GameView(SubView):
    def __init__(self):
        pass

class SidebarView(SubView):
    def __init__(self):
        pass

class MenuView(SubView):
    def __init__(self):
        pass

def initView():
	initWindow()
	initRenderers()
