import os

from .camera import *
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class PyGLApp():
    def __init__(self, screen_posX, screen_posY, screen_width, screen_height) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{screen_posX},{screen_posY}"
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.program_id = None

        pygame.init()
        # pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        # pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        # pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        ##fixing depth buffer aliasing
        #pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 32)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("PyOpenGL Engine")

        self.camera = None
        self.clock = pygame.time.Clock()

    def initialise(self):
        raise NotImplementedError()

    def display(self):
        raise NotImplementedError()

    def camera_init(self):
        raise NotImplementedError()

    def mainloop(self):
        done = False
        self.initialise()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        while not done:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        done = True

            self.camera_init()
            self.display()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
