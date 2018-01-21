import sdl2
import sdl2.ext
import ctypes

def init_window():
    sdl2.ext.init()
    size = get_screensize()
    window = sdl2.ext.Window("Hackathon", size)
    window.show()
    return window



