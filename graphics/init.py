import sdl2
import sdl2.ext
import ctypes

def init_window():
    sdl2.ext.init()
    size = get_screensize()
    window = sdl2.ext.Window("Hackathon", size)
    window.show()
    return window



def get_screensize():
    dm = ctypes.pointer(sdl2.SDL_DisplayMode())
    sdl2.SDL_GetCurrentDisplayMode(0, dm)
    dm = dm.contents
    width = dm.w
    height = dm.h
    return width, height
