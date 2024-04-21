import importlib.resources as pkg_resources

import pymarch.shaders


def get_shader(name: str) -> str:
    shader_name = name + ".glsl"
    s = pkg_resources.read_text(pymarch.shaders, shader_name)
    return s
