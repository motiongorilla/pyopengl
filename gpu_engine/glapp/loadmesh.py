from OpenGL.GL import *
import pygame
from . import mesh, utils

class LoadMesh(mesh.Mesh):
    def __init__(self, filename, program_id, draw_type,
                 color_normals=False, mesh_color=(1.0,1.0,1.0),
                 translation=pygame.Vector3(0,0,0),
                 rotation=mesh.Rotation(0, pygame.Vector3(0,1,0)),
                 scale=pygame.Vector3(1,1,1),
                 animated=False):
        coordinates, triangles, normals, normal_list, uvt, uv_values = self.load_geometry(filename)
        vertices = utils.format_vertices(coordinates, triangles)
        vertex_uvs = utils.format_vertices(uv_values, uvt)
        vertex_normals = utils.format_vertices(normals, normal_list)
        colors = []
        for i in range(len(vertices)):
            colors.append(mesh_color[0])
            colors.append(mesh_color[1])
            colors.append(mesh_color[2])
        if color_normals:
            colors = utils.format_vertices(normals, normal_list)

        super().__init__(program_id=program_id, vertices=vertices,
                         draw_type=draw_type, translation=translation, vertex_colors=colors,
                         rotation=rotation, scale=scale, animated=animated,
                         normals=vertex_normals, uv=vertex_uvs)

    def load_geometry(self, filename):
        vertices = []
        triangles = []
        normals = []
        normal_list = []
        uvt_list = []
        uv_values = []
        with open(filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split(" ")]
                    vertices.append((vx, vy, vz))
                if line[:2] == "vn":
                    vx, vy, vz = [float(value) for value in line[3:].split(" ")]
                    normals.append((vx,vy,vz))
                if line[:2] == "vt":
                    u, v = [float(value) for value in line[3:].split(" ")]
                    uv_values.append((u,v))
                if line[:2] == "f ":
                    t1, t2, t3 = [int(value.split("/")[0]) for value in line[2:].split(" ")]
                    uv1, uv2, uv3 = [int(value.split("/")[1]) for value in line[2:].split(" ")]
                    n1, n2, n3 = [int(value.split("/")[2]) for value in line[2:].split(" ")]
                    triangles.append(t1-1)
                    triangles.append(t2-1)
                    triangles.append(t3-1)

                    normal_list.append(n1-1)
                    normal_list.append(n2-1)
                    normal_list.append(n3-1)

                    uvt_list.append(uv1-1)
                    uvt_list.append(uv2-1)
                    uvt_list.append(uv3-1)
                line = fp.readline()
        return vertices, triangles, normals, normal_list, uvt_list, uv_values
