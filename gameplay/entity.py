from gameplay import physics
from gameplay.physics import Vec2, Polygon
import graphics.sprite
import graphics.render
import graphics.view
import gameplay.state

class Entity:
    def __init__(self, collider: physics.PhysObject, sprite=None):
        self.collider = collider
        self.sprite = sprite

    def processInputEvent(self):
        pass

    def update(self):
        pass

    # directions in sprite sheet order
    # front right back left
    #  0     1     2    3
    def directionFromVelocity(self):
        if (self.collider.vel.x > 0):
            return 1
        if (self.collider.vel.x < 0):
            return 3
        if (self.collider.vel.y < 0):
            return 2
        return 0

    def render(self, renderer):
        pass

class Door(Entity):
    def __init__(self, dir, nextX, nextY, pastX, pastY):
        self.toX = nextX
        self.toY = nextY
        self.fromX = pastX
        self.fromY = pastY
        self.dir = dir
        leftX = 32
        midX = graphics.view.GAME_WIDTH / 2
        rightX = graphics.view.GAME_WIDTH - 32
        topY = 32
        midY = graphics.view.WINDOW_SIZE[1] / 2
        botY = graphics.view.WINDOW_SIZE[1] - 32
        if dir == 0:
            self.collider = physics.PhysObject(Vec2(midX, topY),
                                               Polygon.square(midX, topY, 64, 64), self,
                                               collision_type=physics.collision_types.trigger)
        elif dir == 1:
            self.collider = physics.PhysObject(Vec2(rightX, midY),
                                               Polygon.square(rightX, midY, 64, 64), self,
                                               collision_type=physics.collision_types.trigger)
        elif dir == 2:
            self.collider = physics.PhysObject(Vec2(midX, botY),
                                               Polygon.square(midX, botY, 64, 64), self,
                                               collision_type=physics.collision_types.trigger)
        elif dir == 3:
            self.collider = physics.PhysObject(Vec2(leftX, midY),
                                               Polygon.square(leftX, midY, 64, 64), self,
                                               collision_type=physics.collision_types.trigger)
        self.speed = 0
        self.width = 64
        self.height = 64
        self.sprite = None
        self.loadSprite(dir)

    def loadSprite(self, dir):
        if dir == 0:
            self.sprite = gameplay.state.doorT
        elif dir == 1:
            self.sprite = gameplay.state.doorR
        elif dir == 2:
            self.sprite = gameplay.state.doorB
        elif dir == 3:
            self.sprite = gameplay.state.doorL

    def getSprite(self):
        if (self.sprite == None):
            return
        return graphics.view.SpriteToRender(self.sprite, int(self.collider.pos.x),
                                            int(self.collider.pos.y), 64, 64)
    def to_dict(self):
        return {
            "dir": self.dir,
            "to_x": self.toX,
            "to_y": self.toY,
            "from_x": self.fromX,
            "from_y": self.fromY
        }

    @staticmethod
    def from_dict(dict):
        return Door(dict["dir"], dict["to_x"], dict["to_y"], dict["from_x"], dict["from_y"])

class Ladder(Entity):
    def __init__(self):
        self.collider = physics.PhysObject(Vec2(300, 300),
                                           Polygon.square(300, 300, 16, 16), self,
                                           collision_type=physics.collision_types.trigger)
        self.width = 64
        self.height = 64
        self.speed = 0
        self.collider.add_callback(self.onCollide)
        self.collider.vel.x = 0
        self.collider.vel.y = 0
        self.sprite = None
        self.loadSprite()

    def onCollide(self, collider: physics.PhysObject, other: physics.PhysObject):
        return

    def loadSprite(self):
        self.sprite = gameplay.state.trapDoor

    def getSprite(self):
        if (self.sprite == None):
            return
        return graphics.view.SpriteToRender(self.sprite, 300, 400, 64, 64)

    def to_dict(self):
        return {

        }

    @staticmethod
    def from_dict(dict):
        return Ladder()

class Bullet(Entity):
    def __init__ (self, bullet_id, x, y, direction_x, direction_y):
        print("shooting")
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.id = bullet_id
        self.speed = 80
        self.collider = physics.PhysObject(Vec2(x+direction_x*5, y+direction_y*5), Polygon.square(x+direction_x*5, y+direction_y*5, 10, 10), self, collision_type=physics.collision_types.player)
        self.collider.add_callback(self.onCollide)
        self.collider.vel.x = direction_x * self.speed
        self.collider.vel.y = direction_y * self.speed
        self.load_sprite()
        self.alive = True

    def load_sprite(self):
        self.sprite = graphics.view.sprite_factory.from_file("./assets/players.png").subsprite(graphics.rect.Rect(100, 115, 66, 93))

    def getSprite(self):
        if (self.sprite == None):
            return
        return graphics.view.SpriteToRender(self.sprite, int(self.collider.pos.x), int(self.collider.pos.y))

    def onCollide(self, collider: physics.PhysObject, other: physics.PhysObject):
        if collider.collision_type == physics.collision_types.static or \
           collider.collision_type == physics.collision_types.dynamic or \
           other.collision_type == physics.collision_types.static or \
           other.collision_type == physics.collision_types.dynamic:
            self.alive = False

    def to_dict(self):
        return{
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "d_x": self.direction_x,
            "d_y": self.direction_y
        }

    @staticmethod
    def from_dict(dict):
        return Bullet(dict["id"], dict["x"], dict["y"], dict["d_x"], dict["d_y"])
