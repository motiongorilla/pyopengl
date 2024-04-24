import pygame
from .transformations import *
from .uniform import *

class Light:
    def __init__(self, pos=pygame.Vector3(0,0,0),
                 color=pygame.Vector3(1,1,1), light_id=0) -> None:
        self.transformations = identity_matrix()
        self.position = pos
        self.color = color
        self.light_pos_variable = f"light_data[{light_id}].position"
        self.light_color_variable = f"light_data[{light_id}].color"

    def update(self, program_id):
        light_pos = Uniform("vec3", self.position)
        light_pos.find_variable(program_id, self.light_pos_variable)
        light_pos.load()

        light_color = Uniform("vec3", self.color)
        light_color.find_variable(program_id, self.light_color_variable)
        light_color.load()
