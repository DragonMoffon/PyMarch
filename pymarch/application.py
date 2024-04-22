from arcade import Window
from arcade.camera import CameraData
import arcade.key

from pyglet.math import Vec3

from pymarch.SDFs.sphere import Sphere
from pymarch.march import MarchScene


class MarchWindow(Window):

    def __init__(self):
        super().__init__(1280, 720, "PyMarch Window [1280, 720]", update_rate=1/120)
        a = Sphere(Vec3(150.0, 200.0, -50.0), Vec3(1.0, 0.0, 0.0), 35.0)
        b = Sphere(Vec3(350.0, 300.0, -50.0), Vec3(0.0, 1.0, 0.0), 50.0)
        c = Sphere(Vec3(100.0, 100.0, -50.0), Vec3(0.0, 0.0, 1.0), 100.0)
        camera = CameraData()
        self.march_scene = MarchScene((a, b, c), camera)

    def on_update(self, delta_time: float):
        self.march_scene.do_marches_timed(1/15)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.DELETE:
            self.march_scene.clear()
        return super().on_key_press(symbol, modifiers)

    def on_draw(self):
        self.clear()
        self.march_scene.draw()
