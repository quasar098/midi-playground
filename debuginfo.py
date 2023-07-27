import pygame
import pyperclip

from utils import *
import sys
from platform import system


# noinspection PyBroadException
def print_debug_info():
    debug_info = ""
    debug_info += f"Debug information:\n"
    debug_info += f"os = {system()}\n"
    try:
        debug_info += f"version: {'Binary File' if getattr(sys, 'frozen', False) else 'Source Code'}\n"
    except Exception:
        pass
    debug_info += f"sys.version = {sys.version}\n"
    debug_info += f"framerate = {FRAMERATE}\n"

    for key in Config.__dict__:
        key: str
        v = Config.__dict__[key]
        if key.startswith("__"):
            continue
        if key == "color_themes":
            continue
        if key == "save_attrs":
            v = ", ".join(v)
        debug_info += f"{key} = {v}\n"
    debug_info = debug_info.rstrip("\n")
    print(debug_info)
    pyperclip.copy(debug_info)


def debug_rect(rect: pygame.Rect):
    """Print a copy-pastable equation for debugging in desmos graphing calculator"""
    print(f"\\operatorname\x7Bpolygon\x7D({rect.topleft}, {rect.topright}, {rect.bottomright}, {rect.bottomleft})")


def debug_rectangles(rects: list[pygame.Rect]):
    """Debug rects but multiple"""
    for rect in rects:
        debug_rect(rect)
