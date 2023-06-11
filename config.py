import pygame
from typing import Optional


class Config:

    # constants
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    CAMERA_SPEED = 500
    SQUARE_SIZE = 50
    PARTICLE_SPEED = 10

    # colors
    class Colors:
        wall_color = pygame.Color(60, 63, 65)
        bg_color = pygame.Color(214, 209, 205)
        square_colors = [
            pygame.Color(224, 26, 79),
            pygame.Color(173, 247, 182),
            pygame.Color(249, 194, 46),
            pygame.Color(83, 179, 203)
        ]

    # intended configurable settings
    seed: Optional[int] = None
    midi_file_name: Optional[str] = None
    audio_file_name: Optional[str] = None
    camera_mode: Optional[int] = 2
    start_playing_delay = 3000
    max_notes: Optional[int] = None
    bounce_min_spacing: Optional[float] = 0.03
    square_speed: Optional[int] = 600
    volume: Optional[int] = 50
    music_offset: Optional[int] = -300
    direction_change_chance: Optional[int] = 30
    last_bounce_delay: Optional[float] = 1
    backtrack_chance: Optional[float] = 0.01
    backtrack_amount: Optional[int] = 20
