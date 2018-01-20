import sdl2
import sdl2.ext
import ctypes

WINDOW_SIZE = [1000, 650]
SIDEBAR_WIDTH = 188
GAME_WIDTH = 1000 - SIDEBAR_WIDTH

def initWindow():
    sdl2.ext.init()
    global window
    window = sdl2.ext.Window("Hackathon", WINDOW_SIZE)
    window.show()
    return window


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