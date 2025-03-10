import pygame
from OpenGL.GLU import *
from math import *


class Camera:
    def __init__(self) -> None:
        self.eye = pygame.math.Vector3(0, 0, 0)
        self.up = pygame.math.Vector3(0, 1, 0)
        self.right = pygame.math.Vector3(1, 0, 0)
        self.forward = pygame.math.Vector3(0, 0, 1)
        self.look = pygame.math.Vector3(0, 0, 0)
        self.yaw = -90
        self.pitch = 0
        self.last_mouse = pygame.math.Vector2(0, 0)
        self.update_target()
        self.mouse_sensX = 0.1
        self.mouse_sensY = 0.1

    def update_target(self):
        self.look = self.eye + self.forward

    def rotate(self, pitch, yaw):
        self.yaw += yaw
        self.pitch += pitch
        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0
        self.forward.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward.y = sin(radians(self.pitch))
        self.forward.z = sin(radians(self.yaw)) * cos(radians(self.pitch))

        self.forward = self.forward.normalize()
        self.right = self.forward.cross(pygame.Vector3(0,1,0)).normalize()
        self.up = self.right.cross(self.forward).normalize()

    def update(self, speed, w, h):
        mouse_pos = pygame.mouse.get_pos()
        mouse_change = self.last_mouse - pygame.math.Vector2(mouse_pos)
        pygame.mouse.set_pos(w/2, h/2)

        self.last_mouse = pygame.mouse.get_pos()
        self.rotate(mouse_change.y * self.mouse_sensY, -mouse_change.x * self.mouse_sensX)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            if any((keys[pygame.K_LSHIFT],keys[pygame.K_RSHIFT])):
                self.eye -= self.up * speed
            else:
                self.eye -= self.forward * speed
        elif keys[pygame.K_UP]:
            if any((keys[pygame.K_LSHIFT],keys[pygame.K_RSHIFT])):
                self.eye += self.up * speed
            else:
                self.eye += self.forward * speed
        elif keys[pygame.K_LEFT]:
            self.eye -= self.right * speed
        elif keys[pygame.K_RIGHT]:
            self.eye += self.right * speed

        self.update_target()
        gluLookAt(self.eye.x, self.eye.y, self.eye.z,
                  self.look.x, self.look.y, self.look.z,
                  self.up.x, self.up.y, self.up.z)



