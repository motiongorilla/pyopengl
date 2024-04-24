import pygame
from OpenGL.GLU import *
from math import *
import numpy as np

from .uniform import *
from .transformations import *


class Camera:
    def __init__(self, w, h, fov) -> None:
        self.last_mouse = pygame.math.Vector2(0, 0)
        self.mouse_sensX = 0.1
        self.mouse_sensY = 0.05
        self.speed = 0.1
        self.width = w
        self.height = h

        self.transformation = identity_matrix()
        self.transformation = rotate_complex(self.transformation, angle=35,
                                     axis=pygame.Vector3(0,1,0))
        self.transformation = rotate_complex(self.transformation, angle=20,
                                     axis=pygame.Vector3(-1,0,0))
        self.transformation = translate(self.transformation, 0, 0.5, 10)
        self.projection_matrix = self.perspective_matrix(fov, w/h, 0.01, 10000)

        self.projection = Uniform(data_type="mat4", data=self.projection_matrix)

    def perspective_matrix(self, view_angle, aspect_ratio, near_plane, far_plane):
        a = radians(view_angle)
        d = 1.0/tan(a/2)
        r = aspect_ratio
        b = (far_plane+near_plane)/(near_plane-far_plane)
        c = far_plane * near_plane / (near_plane - far_plane)
        return np.array([[d/r,0,0,0],
                        [0,d,0,0],
                        [0,0,b,c],
                        [0,0,-1,0]], np.float32)


    def rotate(self, pitch, yaw):
        forward_vector = pygame.Vector3(self.transformation[0,2],
                                        self.transformation[1,2],
                                        self.transformation[2,2])
        up_vector = pygame.Vector3(0,1,0)
        angle = forward_vector.angle_to(up_vector)

        self.transformation = rotate(self.transformation, yaw, "Y", False)
        if angle < 170.0 and pitch > 0 or angle > 30.0 and pitch < 0:
            self.transformation = rotate(self.transformation, pitch, "X", True)

    def update(self, program_id):
        mouse_pos = pygame.mouse.get_pos()
        mouse_change = self.last_mouse - pygame.math.Vector2(mouse_pos)
        pygame.mouse.set_pos(self.width/2, self.height/2)

        self.last_mouse = pygame.mouse.get_pos()
        self.rotate(mouse_change.y * self.mouse_sensY, mouse_change.x * self.mouse_sensX)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            if any((keys[pygame.K_LSHIFT],keys[pygame.K_RSHIFT])):
                self.transformation = translate(self.transformation, 0, -self.speed*0.5, 0)
            else:
                self.transformation = translate(self.transformation, 0, 0, self.speed)
        elif keys[pygame.K_UP]:
            if any((keys[pygame.K_LSHIFT],keys[pygame.K_RSHIFT])):
                self.transformation = translate(self.transformation, 0, self.speed*0.5, 0)
            else:
                self.transformation = translate(self.transformation, 0, 0, -self.speed)
        elif keys[pygame.K_LEFT]:
                self.transformation = translate(self.transformation, -self.speed, 0, 0)
        elif keys[pygame.K_RIGHT]:
                self.transformation = translate(self.transformation, self.speed, 0, 0)

        self.projection.find_variable(program_id=program_id, variable_name="projection_mat")
        self.projection.load()
        lookat_matrix = self.transformation
        lookat = Uniform(data_type="mat4", data=lookat_matrix)
        lookat.find_variable(program_id=program_id, variable_name="view_mat")
        lookat.load()
