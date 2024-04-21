from random import randint

from arcade import get_window, draw_point
from arcade.camera import CameraData, PerspectiveProjectionData
from pyglet.math import Vec3

from pymarch.SDFs.marchstruct import MarchStruct
from pymarch.render_target import RenderTarget


SMALL_STEP = Vec3(0.0001, 0.0, 0.0)


class MarchScene:

    def __init__(self, structs: tuple[MarchStruct, ...], camera: CameraData):
        self.march_count: int = 0
        self.max_dist: float = 100.0
        self.max_step: int = 10
        self.intersection_dist: float = 0.0005

        self.light_dir: Vec3 = Vec3(1.0, 0.5, 0.25).normalize()

        self.camera: CameraData = camera

        self.structs: tuple[MarchStruct, ...] = structs
        self.render_target: RenderTarget = RenderTarget(get_window().size)

        self.points = set((x, y) for x in range(self.render_target.size[0]) for y in range(self.render_target.size[1]))

    def _get_world_dist(self, position: Vec3) -> float:
        return min(self.max_dist, min(struct.SDF(position) for struct in self.structs))

    def _get_closest_struct(self, position: Vec3) -> MarchStruct:
        return self.structs[min((struct.SDF(position), idx) for idx, struct in enumerate(self.structs))[-1]]

    def _get_world_normal(self, position: Vec3) -> Vec3:
        grad_x = self._get_world_dist(position + SMALL_STEP.xyy) - self._get_world_dist(position - SMALL_STEP.xyy)
        grad_y = self._get_world_dist(position + SMALL_STEP.yxy) - self._get_world_dist(position - SMALL_STEP.yxy)
        grad_z = self._get_world_dist(position + SMALL_STEP.yyx) - self._get_world_dist(position - SMALL_STEP.yyx)

        return Vec3(grad_x, grad_y, grad_z).normalize()

    def _march_step(self, position: Vec3, direction: Vec3, travel_dist: float, step_count: int):
        if travel_dist >= self.max_dist or step_count > self.max_step:
            return 30, 30, 30

        closest_dist = self._get_world_dist(position)

        if closest_dist <= self.intersection_dist:
            n = self._get_world_normal(position)
            l = max(0.0, n.dot(self.light_dir))
            c = self._get_closest_struct(position).colour
            r, g, b = c * l
            return int(r * 255), int(g * 255), int(b * 255)

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
