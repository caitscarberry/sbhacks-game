import sdl2
import sdl2.ext

from graphics.init import init_window



def main():
    window = init_window()
    running = True
    
    while running == True:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        window.refresh()

main()