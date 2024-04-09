from OpenGL.GL import *
import pygame
import Mesh

class LoadMesh(Mesh.Mesh):
    def __init__(self, filename, draw_type) -> None:
        self.vertices = []
        self.triangles = []
        self.filename = filename
        self.draw_type = draw_type
        self.load_geometry()

    def load_geometry(self):
        with open(self.filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split(" ")]
                    self.vertices.append((vx, vy, vz))
                if line[:2] == "f ":
                    t1, t2, t3 = [int(value.split("/")[0]) for value in line[2:].split(" ")]
                    self.triangles.append(t1-1)
                    self.triangles.append(t2-1)
                    self.triangles.append(t3-1)
                line = fp.readline()
