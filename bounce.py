import pygame
from utils import *


class Bounce:
    def __init__(self, sq_pos: list[float], sq_dir: list[int], time: float, bounce_dir: int):
        self.square_pos = sq_pos  # new square position
        self.square_dir = sq_dir  # new square direction
        self.bounce_dir = bounce_dir  # bounce direction for squish effect; i can't remember if 0 or 1 is horizontal
        self.time = time  # time during bounce

    def get_collision_rect(self):
        sx, sy = self.square_pos
        if self.bounce_dir == 0:
            # bounce left or right wall
            if self.square_dir[0] == -1:
                # right wall
                return pygame.Rect(
                    sx+Config.SQUARE_SIZE/2,
                    sy-10,
                    10,
                    20
                )
            elif self.square_dir[0] == 1:
                # left wall
                return pygame.Rect(
                    sx-10-Config.SQUARE_SIZE/2,
                    sy-10,
                    10,
                    20
                )
        elif self.bounce_dir == 1:
            # bounce top or bottom wall
            if self.square_dir[1] == -1:
                # bottom wall
                return pygame.Rect(
                    sx-10,
                    sy+Config.SQUARE_SIZE/2,
                    20,
                    10
                )
            elif self.square_dir[1] == 1:
                # top wall
                return pygame.Rect(
                    sx-10,
                    sy-10-Config.SQUARE_SIZE/2,
                    20,
                    10
                )

    def copy(self) -> "Bounce":
        return Bounce(self.square_pos, self.square_dir, self.time, self.bounce_dir)

    def __repr__(self):
        return f"<Bounce(sq_pos={self.square_pos}, sq_dir={self.square_dir}, time={self.time}, dir={self.bounce_dir})"
