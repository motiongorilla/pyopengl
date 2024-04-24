from .mesh import *

class Plane(Mesh):
    def __init__(self, animated=False, material=None) -> None:
        vertices = [[1,1,0],
                    [-1,-1,0],
                    [-1,1,0],
                    [-1,-1,0],
                    [1,1,0],
                    [1,-1,0]]
        colors = [
                [1,0,0],
                [1,0,0],
                [1,0,0],
                [1,0,0],
                [1,0,0],
                [1,0,0]]
        super().__init__(vertices=vertices, animated=animated, material=material, vertex_colors=None)
