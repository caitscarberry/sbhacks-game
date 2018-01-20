class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        
    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        
    def __truediv__(self, scalar):
        return Vec2(self.x / scalar, self.y / scalar)

    def __itruediv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    
