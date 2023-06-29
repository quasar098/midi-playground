import pygame
from utils import *
import sys
from platform import system


# noinspection PyBroadException
def print_debug_info():
    print(f"Debug information:")
    print(f"os = {system()}")
    try:
        print(f"version: {'Static' if getattr(sys, 'frozen', False) else 'Source'}")
    except Exception:
        pass
    print(f"sys.version = {sys.version}")
    print(f"framerate = {FRAMERATE}")

    for key in Config.__dict__:
        key: str
        v = Config.__dict__[key]
        if key.startswith("__"):
            continue
        if key == "color_themes":
            continue
        if key == "save_attrs":
            v = ", ".join(v)
        print(f"{key} = {v}")
