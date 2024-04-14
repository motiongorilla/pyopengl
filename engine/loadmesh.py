from OpenGL.GL import *
import pygame
import Mesh

class LoadMesh(Mesh.Mesh):
    def __init__(self, filename, draw_type, position=pygame.Vector3(0,0,0),
                 orientation=Mesh.Rotation(0, pygame.Vector3(1,0,0))) -> None:
        self.filename = filename
        vertices, triangles = self.load_geometry()
        super().__init__(vertices, triangles, draw_type, position, orientation)

    def load_geometry(self)->tuple[list[float],list[float]]:
        vertices = []
        triangles = []
        with open(self.filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split(" ")]
                    vertices.append((vx, vy, vz))
                if line[:2] == "f ":
                    t1, t2, t3 = [int(value.split("/")[0]) for value in line[2:].split(" ")]
                    triangles.append(t1-1)
                    triangles.append(t2-1)
                    triangles.append(t3-1)
                line = fp.readline()
        return vertices, triangles
