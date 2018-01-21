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
import random


class Monster(Entity):
    def __init__(self, monster_id, x, y, type):
        self.id = monster_id
        self.type = type
        self.width = 40
        self.height = 40
        self.speed = 50
        self.next_bullet_id = 0
        self.sprites = []
        self.load_sprite()
        self.collider = physics.PhysObject(Vec2(x, y), Polygon.square(x, y, self.width, self.height),
                                           self, collision_type=physics.collision_types.dynamic)
        self.collider.add_callback(self.onCollide)
        self.alive = True
        self.death_recorded = False

    def onCollide(self, collider: physics.PhysObject, other: physics.PhysObject):
        if other.collision_type == physics.collision_types.player and\
        isinstance(other.owner, Bullet):
            self.alive = False

    def load_sprite(self):
        sprite1 = None
        sprite2 = None
        if self.type == 0:
            sprite1 = graphics.view.sprite_factory.from_file("./assets/sheet_snake_walk.png").subsprite(
                graphics.rect.Rect(6 * 64, 32, 64, 32))
            sprite2 = graphics.view.sprite_factory.from_file("./assets/sheet_snake_walk_flip.png").subsprite(
                graphics.rect.Rect(0, 32, 64, 32))
        elif self.type == 1:
            sprite1 = graphics.view.sprite_factory.from_file("./assets/snail.png").subsprite(
                graphics.rect.Rect(0, 0, 213, 218))
            sprite2 = graphics.view.sprite_factory.from_file("./assets/snail_flip.png").subsprite(
                graphics.rect.Rect(0, 0, 213, 218))

        self.sprites.append(sprite1)
        self.sprites.append(sprite2)
        self.sprites.append(sprite2)
        self.sprites.append(sprite1)

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
        sprite = None
        if self.type == 0:
            sprite = graphics.view.SpriteToRender(self.sprites[self.directionFromVelocity()], int(self.collider.pos.x),
                                                  int(self.collider.pos.y), 64, 32)
        elif self.type == 1:
            sprite = graphics.view.SpriteToRender(self.sprites[self.directionFromVelocity()], int(self.collider.pos.x),
                                                  int(self.collider.pos.y), 64, 64)
        return sprite

    def to_dict(self):
        if (not self.alive):
            self.death_recorded = True
        return {"pos": self.collider.pos.to_dict(), "vel": self.collider.vel.to_dict(), "id": self.id, "type": self.type, "alive": self.alive}

    @staticmethod
    def from_dict(dict):
        pos = Vec2.from_dict(dict["pos"])
        m = Monster(dict["id"], pos.x, pos.y, dict["type"])
        m.collider.vel = Vec2.from_dict(dict["vel"])
        m.alive = dict["alive"]
        if (not m.alive):
            m.death_recorded = True
        return m
