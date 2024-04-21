from random import randint

from arcade import get_window, draw_point
from arcade.camera import CameraData, PerspectiveProjectionData
from pyglet.math import Vec3

from pymarch.SDFs.marchstruct import MarchStruct
from pymarch.render_target import RenderTarget


class MarchScene:

    def __init__(self, structs: tuple[MarchStruct, ...], camera: CameraData):
        self.march_count: int = 0
        self.max_dist: float = 100.0
        self.max_step: int = 10
        self.intersection_dist: float = 0.0005

        self.camera: CameraData = camera

        self.structs: tuple[MarchStruct, ...] = structs
        self.render_target: RenderTarget = RenderTarget(get_window().size)

        self.points = set((x, y) for x in range(self.render_target.size[0]) for y in range(self.render_target.size[1]))

    def _march_step(self, position: Vec3, direction: Vec3, travel_dist: float, step_count: int):
        if travel_dist >= self.max_dist or step_count > self.max_step:
            return 255, 255, 255

        closest_dist = self.max_dist
        closest_struct = None
        for struct in self.structs:
            dist = struct.SDF(position)
            if closest_dist >= dist:
                closest_dist = dist
                closest_struct = struct

        if closest_struct is None:
            return 0, 0, 0

        if closest_dist <= self.intersection_dist:
            r, g, b = closest_struct.colour
            return int(255 * r), int(255 * g), int(255 * b)

        return self._march_step(position + direction * closest_dist, direction, travel_dist+closest_dist, step_count+1)

    def do_marches(self, march_count: int = 1):
        f = Vec3(*self.camera.forward)
        u = Vec3(*self.camera.up)
        r = f.cross(u)

        with self.render_target.activate():
            for _ in range(march_count):
                if not len(self.points):
                    return

                self.march_count += 1
                x, y = self.points.pop()

                start = r * x + u * y
                colour = self._march_step(start, f, 0.0, 0)
                draw_point(x, y, colour, 1)

    def draw(self):
        self.render_target.draw()
