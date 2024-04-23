import pygame
from .transformations import *
from .uniform import *

class Light:
    def __init__(self, program_id, pos=pygame.Vector3(0,0,0), light_id=0) -> None:
        self.transformations = identity_matrix()
        self.program_id = program_id
        self.position = pos
        self.light_variable = f"light_pos[{light_id}]"

    def update(self):
        light_pos = Uniform("vec3", self.position)
        light_pos.find_variable(self.program_id, self.light_variable)
        light_pos.load()
