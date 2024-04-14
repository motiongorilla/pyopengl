from OpenGL.GL import *
import pygame

class Rotation:
    def __init__(self, angle, axis:pygame.Vector3) -> None:
        self.angle = angle
        self.axis = axis

class Mesh:
    def __init__(self, vertices, triangles, draw_type, position, orientation) -> None:
        self.vertices = vertices
        self.triangles = triangles
        self.draw_type = draw_type
        self.position = position
        self.orientation = orientation

    def draw(self, l_width=1.5, l_color=(1,1,1), translate=pygame.Vector3(0,0,0),
             rotate_axis=pygame.Vector3(1,0,0), rotate_angle=0,
             scale=pygame.Vector3(1,1,1))->None:
        glPushMatrix()
        # World rotation
        glRotatef(rotate_angle, rotate_axis.x, rotate_axis.y, rotate_axis.z)
        # Translation
        glTranslatef(translate.x, translate.y, translate.z)
        # Initial position offset
        glTranslatef(self.position.x, self.position.y, self.position.z)
        # Initial rotation/orientation
        glRotatef(self.orientation.angle, self.orientation.axis.x,
                  self.orientation.axis.y, self.orientation.axis.z)
        glScalef(scale.x, scale.y, scale.z)
        for t in range(0, len(self.triangles), 3):
            glLineWidth(l_width)
            glColor3f(l_color[0], l_color[1], l_color[2])
            glBegin(self.draw_type)
            glVertex3fv(self.vertices[self.triangles[t]])
            glVertex3fv(self.vertices[self.triangles[t+1]])
            glVertex3fv(self.vertices[self.triangles[t+2]])
            glEnd()
        glPopMatrix()
