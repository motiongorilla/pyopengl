from .mesh import *

class Axis(Mesh):
    def __init__(self, translation=pygame.Vector3(0,0,0), animated=False, material=None) -> None:
        vertices = [
                    [-100, 0, 0],
                    [100, 0, 0],
                    #X arrow
                    [2, 0, 0],
                    [1.75, 0, 0.25],
                    [2, 0, 0],
                    [1.75, 0, -0.25],
                    # Y Axis
                    [0, -100, 0],
                    [0, 100, 0],
                    #Y arrow
                    [0, 2, 0],
                    [0.25, 1.75, 0],
                    [0, 2, 0],
                    [-0.25, 1.75, 0],
                    # Z Axis
                    [0, 0, -100],
                    [0, 0, 100],
                    # Z arrow
                    [0.25, 0, 1.75],
                    [0, 0, 2],
                    [-0.25, 0, 1.75],
                    [0, 0, 2]]
        colors = [
                    [1.0,0.0,0.0],
                    [1.0,0.0,0.0],
                    [1.0,0.0,0.0],
                    [1.0,0.0,0.0],
                    [1.0,0.0,0.0],
                    [1.0,0.0,0.0],
                    [0.0,1.0,0.0],
                    [0.0,1.0,0.0],
                    [0.0,1.0,0.0],
                    [0.0,1.0,0.0],
                    [0.0,1.0,0.0],
                    [0.0,1.0,0.0],
                    [0.0,0.0,1.0],
                    [0.0,0.0,1.0],
                    [0.0,0.0,1.0],
                    [0.0,0.0,1.0],
                    [0.0,0.0,1.0],
                    [0.0,0.0,1.0],
                    ]
        super().__init__(vertices=vertices,
                         vertex_colors=colors, draw_type=GL_LINES, translation=translation,
                         animated=animated, material=material)
