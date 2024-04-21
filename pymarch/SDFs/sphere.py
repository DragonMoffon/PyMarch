from typing import NamedTuple

from struct import pack

from pyglet.math import Vec3
from pymarch.SDFs.marchstruct import MarchStruct


class Sphere(MarchStruct):

    def __init__(self, position: Vec3, colour: Vec3, radius: float):
        self.position: Vec3 = position
        self.colour: Vec3 = colour
        self.radius: float = radius

    def to_data_struct(self):
        x, y, z = self.position
        R = self.radius
        r, g, b = self.colour
        return pack("fffffff", x, y, z, r, g, b, R)

    def SDF(self, origin: Vec3):
        return (origin - self.position).mag - self.radius


sphere = Sphere(Vec3(0.0, 0.0, 100.0), Vec3(1.0, 0.5, 1.0), 100.0)
