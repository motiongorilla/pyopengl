from OpenGL.GL import *
import pygame

class Mesh:
    def __init__(self, vertices, triangles, draw_type, position) -> None:
        self.vertices = vertices
        self.triangles = triangles
        self.draw_type = draw_type
        self.position = position

    def draw(self, l_width=1.5, l_color=(1,1,1), translate=pygame.Vector3(0,0,0)):
        glPushMatrix()
        glTranslatef(translate.x, translate.y, translate.z)
        glTranslatef(self.position.x, self.position.y, self.position.z)
        for t in range(0, len(self.triangles), 3):
            glLineWidth(l_width)
            glColor3f(l_color[0], l_color[1], l_color[2])
            glBegin(self.draw_type)
            glVertex3fv(self.vertices[self.triangles[t]])
            glVertex3fv(self.vertices[self.triangles[t+1]])
            glVertex3fv(self.vertices[self.triangles[t+2]])
            glEnd()
        glPopMatrix()
