from contextlib import contextmanager

from arcade import get_window, ArcadeContext
import arcade.gl as gl


from pymarch.shader import get_shader


class RenderTarget:

    def __init__(self, size: tuple[int, int]):
        self._ctx: ArcadeContext = get_window().ctx
        self._size = size

        self._colour_texture: gl.Texture2D = self._ctx.texture(size, filter=(gl.NEAREST, gl.NEAREST))
        self._frame_buffer: gl.Framebuffer = self._ctx.framebuffer(color_attachments=self._colour_texture)

        self._render_geometry = gl.geometry.quad_2d_fs()
        self._render_program = self._ctx.program(
            vertex_shader=get_shader("quad_render_vs"),
            fragment_shader=get_shader("quad_render_fs")
        )
        self._render_program['texture0'] = 0

        self._clear_colour: tuple[int, int, int, int] = (0, 0, 0, 0)
        self._clear_depth: float = 0.0
        self._clear_viewport: tuple[int, int, int, int] | None = None

    @property
    def size(self):
        return self._size

    def set_clear_arguments(self, *,
                            colour: tuple[int, int, int, int] | None,
                            depth: float | None,
                            viewport: tuple[int, int, int, int] | None):
        self._clear_colour = colour or (0, 0, 0, 0)
        self._clear_depth = depth or 0.0
        self._clear_viewport = viewport

    @contextmanager
    def activate(self, *, force: bool = False, clear: bool = False):
        previous = self._ctx.active_framebuffer
        try:
            self._frame_buffer.use(force=force)
            get_window().default_camera.use()
            if clear:
                self.clear()
            yield self._frame_buffer
        finally:
            previous.use()
            get_window().default_camera.use()

    def clear(self):
        self._frame_buffer.clear(
            color=self._clear_colour,
            depth=self._clear_depth,
            viewport=self._clear_viewport
        )

    def draw(self):
        self._colour_texture.use(0)
        self._render_geometry.render(self._render_program)
