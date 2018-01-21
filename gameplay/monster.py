from gameplay.entity import Entity
from gameplay.entity import Bullet
import sdl2
from gameplay import physics
from gameplay.physics import Vec2, Polygon
from gameplay.events import GameEvent
from gameplay.controls import ControlsState
import graphics.sprite
import graphics.render
import graphics.view


class Monster(Entity):
    def __init__(self, monster_id, x, y):
        self.id = monster_id
        self.width = 66
        self.height = 50
        self.speed = 50
        self.next_bullet_id = 0
        self.sprite = None
        self.load_sprite()
        self.collider = physics.PhysObject(Vec2(x, y), Polygon.square(x, y, self.width, self.height),
                                           self, collision_type=physics.collision_types.dynamic)

    def load_sprite(self):
        self.sprites = []
        for i in range(0, 4):
            if i == 3 or i == 0:
                self.sprite = graphics.view.sprite_factory.from_file("./assets/sheet_snake_walk.png").subsprite(
                    graphics.rect.Rect(6 * 64, 32, 64, 32))
            else:
                self.sprite = graphics.view.sprite_factory.from_file("./assets/sheet_snake_walk_flip.png").subsprite(
                    graphics.rect.Rect(0, 32, 64, 32))
            self.sprites.append(self.sprite)

    def chooseNewDirection(self, players, room_x, room_y):
        game_event_dict = {
            "type": "MONSTER",
            "monster_id": self.id,
            "pos": self.collider.pos.to_dict()
        }
        min_ind = -1
        min_dist = 10000
        for p in range(len(players)):
            if players[p].roomX != room_x or players[p].roomY != room_y:
                continue
            dist = (players[p].collider.pos - self.collider.pos).length()
            if dist < min_dist:
                min_dist = dist
                min_ind = p

        if min_ind == -1:
            return

        vel = (players[min_ind].collider.pos - self.collider.pos) / min_dist

        self.collider.vel = vel * self.speed

    def getSprite(self):
        if (self.sprite == None):
            return
        return graphics.view.SpriteToRender(self.sprites[self.directionFromVelocity()], int(self.collider.pos.x),
                                            int(self.collider.pos.y))

    def to_dict(self):
        return {"pos": self.collider.pos.to_dict(), "vel": self.collider.vel.to_dict(), "id": self.id}

    @staticmethod
    def from_dict(dict):
        pos = Vec2.from_dict(dict["pos"])
        m = Monster(dict["id"], pos.x, pos.y)
        m.collider.vel = Vec2.from_dict(dict["vel"])
        return m
