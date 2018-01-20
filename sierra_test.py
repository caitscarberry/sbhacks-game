import sdl2
import sdl2.ext
from gameplay.map import getBoard
from graphics.init import init_window


def main():
    map = getBoard(10, 25)
    for i in range(10):
        for j in range(10):
            if map[i][j] is None:
                print(0, end='')
            else:
                print(1, end='')
        print('')
    '''
    window = init_window()
    running = True

    while running == True:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        window.refresh()
    '''


main()