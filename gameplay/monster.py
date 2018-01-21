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

    def chooseNewDirection(self, players):
        game_event_dict = {
            "type": "MONSTER",
            "monster_id": self.id,
            "pos": self.collider.pos.to_dict()
        }
        min_ind = -1
        min_dist = 10000
        for p in range(len(players)):
            dist = (players[p].collider.pos - self.collider.pos).length()
            if dist < min_dist:
                min_dist = dist
                min_ind = p

        if min_ind == -1:
            game_event_dict["code"] = "NONE"
            return GameEvent(game_event_dict)

        vel = (players[min_ind].collider.pos - self.collider.pos) / min_dist

        self.collider.vel = vel * self.speed

        game_event_dict["code"] = "CHANGE_VELOCITY"
        game_event_dict["velocity"] = self.collider.vel.to_dict()

        return GameEvent(game_event_dict)

    def processEvent(self, event):
        if event.params["monster_id"] != self.id:
            return
        self.collider.pos.from_dict(event.params["pos"])

        if "velocity" in event.params:
            self.collider.vel.from_dict(event.params["velocity"])
        elif (event.params["code"] == "SHOOT"):
            # each client is responsible for sending updates about its
            # player's bullets (and ONLY its player's bullets)
            # to the other clients every tick.
            # thus it is safe to have all clients execute the shoot function,
            # because the bullet's position will be quickly corrected if it gets
            # out of sync
            self.shoot(event.params["direction"])

    def shoot(self, direction):
        # each bullet is identified by playerid_bulletnumber
        # this ensures that bullet ids are globally unique
        bullet = Bullet(self.id + "_" + self.next_bullet_id, x, y, direction, self.id)
        self.next_bullet_id += 1

    def getSprite(self):
        if (self.sprite == None):
            return
        return graphics.view.SpriteToRender(self.sprites[self.directionFromVelocity()], int(self.collider.pos.x),
                                            int(self.collider.pos.y))
