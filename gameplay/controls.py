import sdl2
class ControlsState:
    state = {sdl2.SDLK_UP: 0, sdl2.SDLK_DOWN: 0, sdl2.SDLK_RIGHT: 0, sdl2.SDLK_LEFT: 0}
    arrow_keys = [sdl2.SDLK_UP, sdl2.SDLK_DOWN, sdl2.SDLK_RIGHT, sdl2.SDLK_LEFT]

    def should_process_input_event(event):
        if (event.type != sdl2.SDL_KEYDOWN and event.type != sdl2.SDL_KEYUP):
            return True
        if (not event.key.keysym.sym in ControlsState.arrow_keys):
            return False
        if ((event.type == sdl2.SDL_KEYDOWN) and (not ControlsState.state[event.key.keysym.sym])):
            return True
        if (event.type == sdl2.SDL_KEYUP):
            return True

    def update_state(event):
        if (event.type == sdl2.SDL_KEYDOWN):
            ControlsState.state[event.key.keysym.sym] = 1
        elif (event.type == sdl2.SDL_KEYUP):
            ControlsState.state[event.key.keysym.sym] = 0