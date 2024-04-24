from components.PyGLApp import *
from components.utils import *
from components.GraphicsData import GraphicsData
from components.axis import *
from components.loadmesh import *
from components.transformations import *
from components.light import *
from components.material import *
from components.plane import *

import numpy as np

class MeshViewer(PyGLApp):
    def __init__(self) -> None:
        super().__init__(400, 200, 1000, 800)
        self.axis = None
        self.mesh = None
        self.plane = None
        self.lights = []
        # glEnable(GL_CULL_FACE)

    def initialise(self):
        mat = Material("./shaders/texturedvert.vs", "./shaders/texturedfrag.vs")
        vc_mat = Material("./shaders/vertexcolor_vs.vs", "./shaders/vertexcolor_fs.vs")
        grid_mat = Material("./shaders/grid_vs.vs", "./shaders/grid_fs.vs")
        self.axis = Axis(material=vc_mat)
        self.mesh = LoadMesh(material=mat, filename="./geometry/doghouse.obj",
                             texture="./geometry/doghouse_diffuse.png")
        self.plane = Plane(material=grid_mat)

        self.camera = Camera(w=self.screen_width, h=self.screen_height, fov=40)
        self.lights.append(Light(pos=pygame.Vector3(2,1,2), light_id=0))
        self.lights.append(Light(pos=pygame.Vector3(-4,6,2), color=pygame.Vector3(0.3, 1, 0.7), light_id=1))

        glLineWidth(2)
        glEnable(GL_DEPTH_TEST)
        # opacity
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.axis.draw(camera=self.camera)
        # self.plane.draw(camera=self.camera)
        self.mesh.draw(camera=self.camera, lights=self.lights)

MeshViewer().mainloop()
