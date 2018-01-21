import sdl2
import sdl2.ext
from gameplay.floor import Floor

from graphics.init import init_window


def main():
    '''
    map = getBoard(10, 25)
    for i in range(10):
        for j in range(10):
            if map[i][j] is None:
                print(0, end='')
            else:

                print(1, end='')
        print('')

    '''
    f = Floor()
    f.genFloor(10, 25)
    print(f)


main()