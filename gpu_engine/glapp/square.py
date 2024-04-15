from .mesh import *

class Square(Mesh):
    def __init__(self, program_id, location) -> None:
        vertices = [[0.5, 0.5, -1.0],
                [0.5, -0.5, -1.0],
                [-0.5, -0.5, -1.0],
                [-0.5, 0.5, -1.0]]
        colors = [[1, 0, 0],
                [1, 0.5, 0],
                [1, 1, 0],
                [0, 1, 0.5]]
        super().__init__(program_id=program_id, vertices=vertices,
                         vertex_colors=colors, draw_type=GL_TRIANGLE_FAN, translation=location)
