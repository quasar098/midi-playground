import moderngl
import pygame
from typing import Optional, Any
from json import load, dump
from os.path import isfile


class Config:
    # constants
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    CAMERA_SPEED = 500
    SQUARE_SIZE = 50
    PARTICLE_SPEED = 10

    # colors
    #
    # each color theme requires a hallway color, a background color, and at least one square color
    # optionally, the color theme provides an hp_bar_border color (default 10, 9, 8),
    # an hp_bar_background color (default 34, 51, 59), and a list
    # of hp_bar_fill colors (default (156, 198, 155), (189, 228, 168), (215, 242, 186))
    #
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
        },
        "green-screen-hallway": {
            "hallway": pygame.Color(0, 255, 0),
            "background": pygame.Color(60, 63, 65),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
            ]
        },
        "green-screen-background": {
            "hallway": pygame.Color(60, 63, 65),
            "background": pygame.Color(0, 255, 0),
            "square": [
                pygame.Color(224, 26, 79),
                pygame.Color(173, 247, 182),
                pygame.Color(249, 194, 46),
                pygame.Color(83, 179, 203)
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
    volume: Optional[int] = 70
    music_offset: Optional[int] = -300
    direction_change_chance: Optional[int] = 30
    hp_drain_rate = 10
    theatre_mode = False
    particle_trail = True
    botplay = False
    fullscreen = True
    shader_file_name = "none.glsl"

    # settings that are not configurable (yet)
    backtrack_chance: Optional[float] = 0.02
    backtrack_amount: Optional[int] = 40
    rainbow_speed: Optional[int] = 30
    square_swipe_anim_speed: Optional[int] = 4
    particle_amount = 10

    # other random stuff
    current_song = None
    ctx: moderngl.Context = None
    glsl_program: moderngl.Program = None
    render_object: moderngl.VertexArray = None
    screen: pygame.Surface = None
    dt = 0.01

    # ascii shader
    ascii_tex: moderngl.Texture = None

    # keys to save and load
    save_attrs = ["theme", "seed", "camera_mode", "start_playing_delay", "max_notes", "bounce_min_spacing",
                  "square_speed", "volume", "music_offset", "direction_change_chance", "hp_drain_rate", "theatre_mode",
                  "particle_trail", "shader_file_name", "botplay", "fullscreen"]


def get_colors():
    return Config.color_themes.get(Config.theme, "dark")


def save_to_file(dat: Optional[dict[str, Any]] = None):
    if dat is None:
        dat = {k: getattr(Config, k) for k in Config.save_attrs}
    with open("./assets/settings.json", "w") as f:
        dump(dat, f)

def is_botplay():
    return Config.botplay
def load_from_file():
    try:
        if isfile("./assets/settings.json"):
            with open("./assets/settings.json", "r") as f:
                data = load(f)
                for setting in data:
                    setattr(Config, setting, data[setting])
        else:
            with open("./assets/settings.json", "w") as f:
                f.write("{}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "config":
    load_from_file()
