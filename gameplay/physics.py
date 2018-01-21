from math import sqrt
import math
from enum import Enum
from typing import Sequence
import sys
class Vec2:
    __slots__ = ["x", "y"]
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    
    def length(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def squarelength(self):
        return self.x * self.x + self.y * self.y
    
    def perpendicular(self):
        return Vec2(-self.y, self.x)

    def normalize(self):
        dist = self.length()
        return Vec2(self.x / dist, self.y / dist)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
        
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
        
    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        return self
        
    def __truediv__(self, scalar):
        return Vec2(self.x / scalar, self.y / scalar)

    def __itruediv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        return self
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def to_dict(self):
        return {"x": self.x, "y": self.y}

    def from_dict(self, dictionary):
        self.x = dictionary["x"]
        self.y = dictionary["y"]

    
class AABB:
    __slots__ = ["left", "right", "top", "bottom"]
    def __init__(self, x, y, w, h):
        self.left = x
        self.top = y
        self.right = x + w
        self.bottom = y + h

    def intersects(self, other):
        return not (other.left > self.right or \
                    other.right < self.left or \
                    other.top > self.bottom or \
                    other.bottom < self.top)

    def extend(self, distance: Vec2):
        left, right = self.left, self.right
        top, bottom = self.top, self.bottom
        if distance.x < 0: # Negative X
            left += distance.x
        else:
            right += distance.x
        if distance.y < 0: # Negative Y
            top += distance.y
        else:
            bottom += distance.y
        return AABB(left, top, right - left, bottom - top)

    def __repr__(self):
        return "[({}, {}), ({}, {})]".format(self.left, self.top, self.right, self.bottom)
    

class LineSegment:
    __slots__ = ["start", "stop"]
    
    def __init__(self, start, stop):
        self.start = min(start, stop)
        self.stop = max(start, stop)

    def overlap(self, other) -> float:
        return max(0.0, min(self.stop, other.stop) - max(self.start, other.start))

    def __repr__(self):
        return "({}, {})".format(self.start, self.stop)

    
class Polygon:
    def __init__(self, verts: Sequence[Vec2]):
        if len(verts) < 3:
            raise ValueError("A polygon must have at least 3 axes, only {} given".format(len(axes)))

        self.verts = verts
        

    def get_aabb(self):
        ax0 = self.verts[0]
        minx = maxx = ax0.x
        miny = maxy = ax0.y
        for v in self.verts:
            minx = min(minx, v.x)
            maxx = max(maxx, v.x)
            miny = min(miny, v.y)
            maxy = max(maxy, v.y)

        return AABB(minx, miny, maxx - minx, maxy - miny)

    def project(self, axis:Vec2):
        low = high = self.verts[0].dot(axis)
        for vec in self.verts:
            low = min(low, vec.dot(axis))
            high = max(high, vec.dot(axis))

        return LineSegment(low, high)
        
    def move(self, distance:Vec2):
        for v in self.verts:
            v += distance
            
    @staticmethod
    def square(x, y, w, h):
        axes = [Vec2(x, y), Vec2(x + w, y), Vec2(x + w, y + h), Vec2(x, y + h)]
        return Polygon(axes)
        
    def __str__(self):
        return ", ".join([str(point) for point in self.verts])

collision_types = Enum("collision_type", ["static", "dynamic"])
class PhysObject:
    def __init__(self, pos, collision: Polygon, vel: Vec2=None, collision_type=collision_types.static, callback: callable=None):
        self.pos = pos
        self.vel = vel or Vec2()
        self.callback = callback
        self.collision = collision
        self.collision_type = collision_type
        

    @property
    def aabb(self):
        return self.collision.get_aabb()


class Simulation:
    def __init__(self):
        self.objects = set()
        

    def step(self, dt):
        for obj in self.objects:
            distance = obj.vel * dt
            #print(distance)
            #print(obj.pos)
            if obj.collision_type == collision_types.dynamic:
                self.move_object(obj, distance)
        
    def add_object(self, obj):
        self.objects.add(obj)
        
    def move_object(self, obj: PhysObject, distance: Vec2):
        extended_box = obj.aabb.extend(distance)
        print("Extended aabb", extended_box)
        collisions = []
        # Get all possible collisions

        for other in self.objects:
            # Don't collide with yourself
            if other is obj:
                continue

            if extended_box.intersects(other.aabb):
                print("Collision?")
                collisions.append((other, other.pos - obj.pos))
                
        collisions.sort(key=lambda x: x[1].squarelength())
        print(collisions)
        print(distance)
        # Do SAT until we get any collisions
        obj.pos += distance
        obj.collision.move(distance)
        for key, dist in collisions:
            minvec = self.sat(obj.collision, key.collision)
            if minvec:
                print(minvec)
                
                # The distance the object can move is as much of its movement as possible,
                # then shift it by the MTGV
                obj.pos -= minvec
                obj.collision.move(-minvec)
                print("Collides!")
                #sys.exit(0)
                return
        
        #print(obj.pos)
        

    def sat(self, first: Polygon, second: Polygon):
        axes = []
        for i in range(len(first.verts)):
            axes.append((first.verts[(i + 1) % len(first.verts)] - first.verts[i]).perpendicular().normalize())
        for i in range(len(second.verts)):
            axes.append((second.verts[(i + 1) % len(second.verts)] - second.verts[i]).perpendicular().normalize())
        #print(first.verts)
        #print(second.verts)
        #print(axes)
        bestaxis = None
        overlap = math.inf
        for axis in axes:
            seg1 = first.project(axis)
            seg2 = second.project(axis)
            #print(seg1, seg2)
            o = seg1.overlap(seg2)
            #print(o)
            if o == 0.0: # No overlap, no collision
                return None
            elif o < overlap:
                overlap = o
                bestaxis = axis
        print(axis, overlap)
        return axis.normalize() * overlap
