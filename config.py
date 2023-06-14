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
    color_themes = {
        "dark": {
            "hallway": pygame.Color(214, 209, 205),
            "background": pygame.Color(60, 63, 65),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        # credits to TheCodingCrafter for these themes
        "light": {
            "hallway": pygame.Color(60, 63, 65),
            "background": pygame.Color(214, 209, 205),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "rainbow": {
            "hallway": pygame.Color((214, 209, 205)),
            "background": pygame.Color((60, 63, 65)),
            "square": [
                pygame.Color(0, 0, 0)
            ]
        },
        "autumn": {
            "hallway": pygame.Color((252, 191, 73)),
            "background": pygame.Color((247, 127, 0)),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "winter": {
            "hallway": pygame.Color((202, 240, 255)),
            "background": pygame.Color((0, 180, 216)),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "spring": {
            "hallway": pygame.Color((158, 240, 26)),
            "background": pygame.Color((112, 224, 0)),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "magenta": {
            "hallway": pygame.Color((239, 118, 116)),
            "background": pygame.Color((218, 52, 77)),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "monochromatic": {
            "hallway": pygame.Color((255, 255, 255)),
            "background": pygame.Color((0, 0, 0)),
            "square": [
                pygame.Color(80, 80, 80),
                pygame.Color(150, 150, 150),
                pygame.Color(100, 100, 100),
                pygame.Color(200, 200, 200)
            ]
        }
    }

    # intended configurable settings
    theme: Optional[str] = "dark"
    seed: Optional[int] = None
    camera_mode: Optional[int] = 2
    start_playing_delay = 3000
    max_notes: Optional[int] = None
    bounce_min_spacing: Optional[float] = 30
    square_speed: Optional[int] = 600
    volume: Optional[int] = 30
    music_offset: Optional[int] = -300
    direction_change_chance: Optional[int] = 30

    # settings that are not configurable (yet)
    backtrack_chance: Optional[float] = 0.01
    rainbow_speed: Optional[int] = 30
    backtrack_amount: Optional[int] = 40

    # just global stuff
    midi_file_name: Optional[str] = None
    audio_file_name: Optional[str] = None


def get_colors():
    return Config.color_themes.get(Config.theme, "dark")
