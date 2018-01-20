import sdl2

class Rect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.rect = sdl2.SDL_Rect(x, y, w, h)

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, val):
        self.rect.x = val
        
    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, val):
        self.rect.y = val
        
    @property
    def width(self):
        return self.rect.w

    @width.setter
    def width(self, val):
        self.rect.w = val

    @property
    def height(self):
        return self.rect.h

    @height.setter
    def height(self, val):
        self.rect.h = val
        
    def contains(self, other):
        return self.x <= other.x and self.width >= other.width and \
            self.y <= other.y and self.height >= other.height
    
