import pygame
from utils import *
from bounce import Bounce


class Square:
    def __init__(self, x: float = 0, y: float = 0, dx: int = 1, dy: int = 1):
        self.pos: list[float] = [x, y]
        self.dir: list[int] = [dx, dy]
        self.last_bounce_time = -100
        self.latest_bounce_direction = 0  # 0 = horiz, 1 = vert
        self.past_colors = []

    def register_past_color(self, col: tuple[int, int, int]):
        self.past_colors.insert(0, col)
        self.past_colors.insert(0, col)
        self.past_colors.insert(0, col)
        while len(self.past_colors) > Config.SQUARE_SIZE*4/5:
            self.past_colors.pop()

    def get_surface(self, size: tuple[int, int]):
        ss = int(Config.SQUARE_SIZE*4/5)
        surf = pygame.Surface((ss, ss))
        for index, col in enumerate(self.past_colors):
            y = index if self.dir_y != 1 else ss-1-index
            pygame.draw.line(surf, col, (0, y), (ss, y))
        return pygame.transform.scale(surf, size)

    def copy(self) -> "Square":
        new = Square(*self.pos, *self.dir)
        new.last_bounce_time = self.last_bounce_time
        new.latest_bounce_direction = self.latest_bounce_direction
        return new

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @x.setter
    def x(self, val: int):
        self.pos[0] = val

    @y.setter
    def y(self, val: int):
        self.pos[1] = val

    @property
    def dir_x(self):
        return self.dir[0]

    @property
    def dir_y(self):
        return self.dir[1]

    @property
    def rect(self):
        return pygame.Rect(self.x-Config.SQUARE_SIZE/2, self.y-Config.SQUARE_SIZE/2, *([Config.SQUARE_SIZE]*2))

    def obey_bounce(self, bounce: Bounce):
        # planned bounces
        self.pos = bounce.square_pos
        self.dir = bounce.square_dir
        self.latest_bounce_direction = bounce.bounce_dir
        self.last_bounce_time = bounce.time
        return

    def reg_move(self):
        self.x += self.dir_x*Config.square_speed/FRAMERATE
        self.y += self.dir_y*Config.square_speed/FRAMERATE
