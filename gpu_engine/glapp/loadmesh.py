from OpenGL.GL import *
import pygame
from . import mesh, utils

class LoadMesh(mesh.Mesh):
    def __init__(self, filename, program_id, draw_type,
                 color_normals=False, mesh_color=(1,1,1),
                 translation=pygame.Vector3(0,0,0),
                 rotation=mesh.Rotation(0, pygame.Vector3(0,1,0)),
                 scale=pygame.Vector3(1,1,1),
                 animated=False):
                 # rotation_anim=mesh.Rotation(0, pygame.Vector3(0,1,0)),
                 # translate_anim=pygame.Vector3(0,0,0),
                 # scale_anim=pygame.Vector3(1,1,1)) -> None:
        coordinates, triangles, normals, normal_list = self.load_geometry(filename)
        vertices = utils.format_vertices(coordinates, triangles)
        colors = []
        for i in range(len(vertices)):
            colors.append(mesh_color[0])
            colors.append(mesh_color[1])
            colors.append(mesh_color[2])
        if color_normals:
            colors = utils.format_vertices(normals, normal_list)

        super().__init__(program_id=program_id, vertices=vertices,
                         draw_type=draw_type, translation=translation, vertex_colors=colors,
                         rotation=rotation, scale=scale, animated=animated)
                         # rotation_anim=rotation_anim,
                         # translate_anim=translate_anim, scale_anim=scale_anim)

    def load_geometry(self, filename):
        vertices = []
        triangles = []
        normals = []
        normal_list = []
        with open(filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split(" ")]
                    vertices.append((vx, vy, vz))
                if line[:2] == "vn":
                    r, g, b = [abs(float(value)) for value in line[3:].split(" ")]
                    normals.append((r,g,b))
                if line[:2] == "f ":
                    t1, t2, t3 = [int(value.split("/")[0]) for value in line[2:].split(" ")]
                    n1, n2, n3 = [int(value.split("/")[2]) for value in line[2:].split(" ")]
                    triangles.append(t1-1)
                    triangles.append(t2-1)
                    triangles.append(t3-1)

                    normal_list.append(n1-1)
                    normal_list.append(n2-1)
                    normal_list.append(n3-1)
                line = fp.readline()
        return vertices, triangles, normals, normal_list
