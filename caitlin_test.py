import sdl2
import sdl2.ext
import sdl2.ext.sprite
from sdl2.ext.color import Color
from graphics.init import init_window
import graphics.sprite
import graphics.render
from gameplay.entity import Player

class ControlsState:
    def __init__(self):
        self.state = {sdl2.SDLK_UP: False, sdl2.SDLK_DOWN: False, sdl2.SDLK_RIGHT: False, sdl2.SDLK_LEFT: False}
        self.arrow_keys = [sdl2.SDLK_UP, sdl2.SDLK_DOWN, sdl2.SDLK_RIGHT, sdl2.SDLK_LEFT]

    def should_process_input_event(self, event):
        if (event.type != sdl2.SDL_KEYDOWN and event.type != sdl2.SDL_KEYUP):
            return True
        if (not event.key.keysym.sym in self.arrow_keys):
            return False
        return ((event.type == sdl2.SDL_KEYDOWN) and (not self.state[event.key.keysym.sym])) or ((event.type == sdl2.SDL_KEYUP) and (self.state[event.key.keysym.sym]))

    def update_state(self, event):
        if (event.type == sdl2.SDL_KEYDOWN):
            self.state[event.key.keysym.sym] = True
        elif (event.type == sdl2.SDL_KEYUP):
            self.state[event.key.keysym.sym] = False
 
def main():
    window = init_window()
    running = True
    render = sdl2.ext.sprite.Renderer(window)
    my_render = graphics.render.Renderer(render)
    col = Color(123, 123, 123)
    playersprite = graphics.sprite.Sprite.from_file("./assets/players.png")
    player = Player(0, 0, 0)
    controls_state = ControlsState()
    while running == True:
        events = sdl2.ext.get_events()
        render.clear(col)
        my_render.draw_sprite(playersprite, player.x, player.y)
        player_events = []
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            else:
                if controls_state.should_process_input_event(event):
                    player_event = player.processInputEvt(event)
                    player_events.append(player_event)
                    controls_state.update_state(event)
                    #broadcast player event
        for event in player_events:
            player.processPlayerEvt(event)
        player.update()
        render.present()
        window.refresh()
        sdl2.SDL_Delay(16)

if __name__ == "__main__":
    main()
