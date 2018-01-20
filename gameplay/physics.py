from math import sqrt
import math
from enum import Enum
from typing import Sequence

class Vec2:
    __slots__ = ["x", "y"]
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


    def length(self):
        return sqrt(self.x * self.x + self.y + self.y)

    def squarelength(self):
        return self.x * self.x + self.y * self.y
    
    def perpendicular(self):
        return Vec2(-self.y, self.x)

    def normalize(self):
        dist = self.length()
        return Vec2(self.x / dist, self.y / dist)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def __str__(self):
        return "({}, {})".format(self.x, self.y)
    
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

    
class AABB:
    __slots__ = ["x1", "y1", "x2", "y2"]
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def intersects(self, other):
        return self.x1 <= other.x1 and self.x2 <= other.x2 \
            and self.y1 <= other.y1 and self.y2 <= other.y2

    def extend(self, distance: Vec2):
        x1, x2 = self.x1, self.x2
        y1, y2 = self.y1, self.y2
        if distance.x < 0: # Negative X
            x1 += distance.x
        else:
            x2 += distance.x
        if distance.y < 0: # Negative Y
            y1 += distance.y
        else:
            y2 += distance.y
        return AABB(x1, y1, x2 - x1, y2 - y1)
    


class LineSegment:
    __slots__ = ["start", "stop"]
    
    def __init__(self, start, stop):
        self.start = min(start, stop)
        self.stop = max(start, stop)

    def overlap(self, other: LineSegment) -> float:
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
        
    
    @classmethod
    def square(self, x, y, w, h):
        axes = [Vec2(x, y), Vec2(x + w, y), Vec2(x + w, y + h), Vec2(x, y + h)]
        return Polygon(axes)
        
    def __str__(self):
        return ", ".join([str(point) for point in self.verts])
    
class PhysObject:
    collision_types = Enum("collision_type", ["static", "dynamic"])
    def __init__(self, pos, collision: Polygon, vel: Vec2=None, callback: callable=None):
        self.pos = pos
        self.vel = vel or Vec2()
        self.callback = callback
        self.collision = collision
        self.aabb = collision.get_aabb()
        self.collision_type = PhysObject.collision_types.static


class Simulation:
    def __init__(self):
        self.objects = set()


    def detect_collisions(self):
        pass
                
    def move_object(self, obj: PhysObject, distance: Vec2):
        extended_box = obj.aabb.extend(distance)
        collisions = []
        # Get all possible collisions
        for other in self.objects:
            if other is obj:
                continue

            if extended_box.intersects(other.aabb):
                collisions.append((other, other.pos - obj.pos))
        collisions.sort(key=lambda x: x[1].squaredistance())

        # Do SAT until we get any collisions
        obj.pos += distance
        for key, dist in collisions:
            minvec = self.sat(obj, key)
            if minvec:
                # The distance the object can move is as much of its movement as possible,
                # then shift it by the MTGV
                obj.pos -= minvec
        
                
        

    def sat(self, first: Polygon, second: Polygon):
        axes = []
        for i in range(len(first.verts)):
            axes.append((first.verts[(i + 1) % len(first.verts)] - first.verts[i]).perpendicular())
        for i in range(len(second.verts)):
            axes.append((second.verts[(i + 1) % len(second.verts)] - second.verts[i]).perpendicular())

        bestaxis = None
        overlap = math.inf
        for axis in axes:
            seg1 = first.project(axis)
            seg2 = second.project(axis)
            o = seg1.overlap(seg2)
            if o == 0.0: # No overlap, no collision
                return None
            elif o < overlap:
                overlap = o
                bestaxis = axis

        return axis.normalize() * overlap


        
