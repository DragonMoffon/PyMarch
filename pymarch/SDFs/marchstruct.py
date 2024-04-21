from pyglet.math import Vec3


class MarchStruct:

    def to_data_struct(self):
        raise NotImplementedError()

    def SDF(self, origin: Vec3):
        raise NotImplementedError()