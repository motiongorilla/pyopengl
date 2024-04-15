from .mesh import *
from . import utils
import numpy as np

class Cube(Mesh):
    def __init__(self, program_id, location) -> None:
        coordinates = [(0.5, -0.5, 0.5),
                         (-0.5, -0.5, 0.5),
                         (0.5, 0.5, 0.5),
                         (-0.5, 0.5, 0.5),
                         (0.5, 0.5, -0.5),
                         (-0.5, 0.5, -0.5),
                         (0.5, -0.5, -0.5),
                         (-0.5, -0.5, -0.5),
                         (0.5, 0.5, 0.5),
                         (-0.5, 0.5, 0.5),
                         (0.5, 0.5, -0.5),
                         (-0.5, 0.5, -0.5),
                         (0.5, -0.5, -0.5),
                         (0.5, -0.5, 0.5),
                         (-0.5, -0.5, 0.5),
                         (-0.5, -0.5, -0.5),
                         (-0.5, -0.5, 0.5),
                         (-0.5, 0.5, 0.5),
                         (-0.5, 0.5, -0.5),
                         (-0.5, -0.5, -0.5),
                         (0.5, -0.5, -0.5),
                         (0.5, 0.5, -0.5),
                         (0.5, 0.5, 0.5),
                         (0.5, -0.5, 0.5)
                         ]
        triangles = [0, 2, 3, 0, 3, 1, 8, 4, 5, 8, 5, 9, 10, 6, 7, 10, 7, 11, 12,
                          13, 14, 12, 14, 15, 16, 17, 18, 16, 18, 19, 20, 21, 22, 20, 22, 23]
        vertices = utils.format_vertices(coordinates, triangles)
        colors = np.random.uniform(low=0.0, high=1.0, size=(36,3))
        super().__init__(program_id=program_id, vertices=vertices,
                         vertex_colors=colors, draw_type=GL_TRIANGLES, translation=location)
