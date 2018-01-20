import sdl2
import sdl2.ext
import sdl2.ext.sprite
from sdl2.ext.color import Color
from graphics.init import init_window
import graphics.sprite
import graphics.render
from gameplay.entity import Player

def main():
    window = init_window()
    running = True
    render = sdl2.ext.sprite.Renderer(window)
    my_render = graphics.render.Renderer(render)
    col = Color(123, 123, 123)
    playersprite = graphics.sprite.Sprite.from_file("./assets/players.png")
    player = Player(0, 0, 0)
    while running == True:
        events = sdl2.ext.get_events()
        render.clear(col)
        my_render.draw_sprite(playersprite, player.x, player.y)
        print(player.x, player.y)
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            render.present()
        window.refresh()
        sdl2.SDL_Delay(16)

if __name__ == "__main__":
    main()
