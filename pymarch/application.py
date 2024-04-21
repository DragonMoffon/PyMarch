from arcade import Window
from arcade.camera import CameraData

from pyglet.math import Vec3

from pymarch.SDFs.sphere import Sphere
from pymarch.march import MarchScene


class MarchWindow(Window):

    def __init__(self):
        super().__init__(1280, 720, "PyMarch Window [1280, 720]")
        a = Sphere(Vec3(300.0, 150.0, -30.0), Vec3(1.0, 0.0, 0.0), 50.0)
        b = Sphere(Vec3(200.0, 400.0, -20.0), Vec3(0.0, 1.0, 0.0), 15.0)
        c = Sphere(Vec3(0, 0, -50.0), Vec3(0.0, 0.0, 1.0), 250.0)
        camera = CameraData()
        self.march_scene = MarchScene((a, b, c), camera)

    def on_update(self, delta_time: float):
        self.march_scene.do_marches(500)

    def on_draw(self):
        self.clear()
        self.march_scene.draw()
