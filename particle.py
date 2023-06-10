import random
from utils import *
import pygame


class Particle:
    def __init__(self, pos: list[float], delta: list[float]):
        self.pos = pos.copy()
        self.size = random.randint(7, 14)
        self.delta = delta.copy()
        self.delta[0] += random.randint(-4, 4)/8
        self.delta[1] += random.randint(-4, 4)/8

    def age(self):
        self.size -= 15/FRAMERATE
        self.x += self.delta[0] * Config.PARTICLE_SPEED
        self.y += self.delta[1] * Config.PARTICLE_SPEED
        self.x = self.x * 1-(10/FRAMERATE)
        self.y = self.y * 1-(10/FRAMERATE)
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