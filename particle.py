import random
from utils import *
import pygame


class Particle:
    SPEED_VARIATION = 4
    SIZE_MIN = 7
    SIZE_MAX = 14
    AGE_RATE = 20
    SLOW_DOWN_RATE = 1.2

    def __init__(self, pos: list[float], delta: list[float], invert_color: bool = False):
        self.pos = pos.copy()
        self.size = random.randint(Particle.SIZE_MIN, Particle.SIZE_MAX)
        self.delta = delta.copy()
        self.delta[0] += random.randint(-Particle.SPEED_VARIATION, Particle.SPEED_VARIATION)/8
        self.delta[1] += random.randint(-Particle.SPEED_VARIATION, Particle.SPEED_VARIATION)/8
        # color is hallway color if invert_color is false, else it's background color
        self.color = get_colors()["hallway"] if not invert_color else get_colors()["background"]

    def age(self):
        self.size -= Particle.AGE_RATE*Config.dt
        self.x += self.delta[0] * Config.PARTICLE_SPEED
        self.y += self.delta[1] * Config.PARTICLE_SPEED
        self.delta[0] /= (Particle.SLOW_DOWN_RATE+FRAMERATE) * Config.dt
        self.delta[1] /= (Particle.SLOW_DOWN_RATE+FRAMERATE) * Config.dt
        return self.size <= 0

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, val: float):
        self.pos[0] = val

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, val: float):
        self.pos[1] = val

    @property
    def rect(self):
        return pygame.Rect(self.x-self.size/2, self.y-self.size/2, *(2*[self.size]))