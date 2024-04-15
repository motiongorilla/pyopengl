from .mesh import *

class Triangle(Mesh):
    def __init__(self, program_id, location) -> None:
        vertices = [
                [-0.5, -0.25, 0],
                [0, 0.75, 0],
                [0.5, -0.25, 0]
                ]
        colors = [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
                ]
        super().__init__(program_id=program_id, vertices=vertices,
                         vertex_colors=colors, draw_type=GL_TRIANGLES, translation=location)
