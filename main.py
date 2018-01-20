import sdl2
import sdl2.ext
import sdl2.ext.sprite
from sdl2.ext.color import Color
from graphics.init import init_window



def main():
    window = init_window()
    running = True
    render = sdl2.ext.sprite.Renderer(window)
    col = Color(123, 123, 123)
    while running == True:
        events = sdl2.ext.get_events()
        render.clear(col)
        render.draw_rect((340, 340, 200, 200), Color(r=255))
        
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        render.present()
        window.refresh()

if __name__ == "__main__":
    main()
