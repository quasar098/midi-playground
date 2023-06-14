from typing import Union, Optional
import mido
import pygame
from sys import platform
from enum import Enum
from config import Config, get_colors
from os.path import join
from math import sin, pi
from sys import setrecursionlimit
from time import time as get_current_time
setrecursionlimit(10000)  # increase if more notes


class UserCancelsLoading(Exception):
    """User cancels the loading screen"""
    pass


# vsync framerate if on windows, else 60
try:
    import win32api
    FRAMERATE = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1).DisplayFrequency
except ModuleNotFoundError:
    if platform == "win32":
        print("The win32api python module is not found! Install it with \"pip install pywin32\"")
    FRAMERATE = 60


# camera follow modes
class CameraFollow(Enum):
    Center = 0  # center the square
    Lazy = 1  # lazy camera, used by Crazy Nutter 101
    Smoothed = 2  # smoothed camera, interpolates camera a little bit between current and previous every frame
    Predictive = 3  # smoothed camera, but you can see where the square will bounce better


# noinspection PyUnresolvedReferences
def read_midi_file(filename):
    midi_file = mido.MidiFile(filename)

    notes = []
    current_time = 0

    for msg in midi_file:
        if msg.type == 'note_on' and msg.velocity != 0:
            note = msg.note
            timestamp = current_time + msg.time
            notes.append((note, round(timestamp*1000)/1000, msg.channel))
        current_time += msg.time
    return notes


# remove values that are too close to each other
def remove_too_close_values(lst: list[float], threshold=30) -> list[float]:
    """Assumes the list is sorted"""
    new = []
    before = None
    for _ in lst:
        if before is None:
            before = _
            new.append(_)
            continue
        if before+threshold/1000 > _:
            continue
        before = _
        new.append(_)
    return new


def debug_rect(rect: pygame.Rect):
    """Print a copy-pastable equation for debugging in desmos graphing calculator"""
    print(f"\\operatorname\x7Bpolygon\x7D({rect.topleft}, {rect.topright}, {rect.bottomright}, {rect.bottomleft})")


_font_registry: dict[str, pygame.font.Font] = {}


def get_font(font_name: str, size: int = 24) -> pygame.font.Font:
    fn_id = f"[{font_name}/{size}]"
    if fn_id not in _font_registry:
        try:
            _font_registry[fn_id] = pygame.font.Font(font_name, size)
        except FileNotFoundError:
            print(f"Font {fn_id} not found!")
            _font_registry[fn_id] = pygame.font.SysFont("Arial", size)
    return _font_registry[fn_id]


_channels = []
_sound_registry: dict[str, pygame.mixer.Sound] = {}


def play_sound(snd_name: str, vol: float = 0.5):
    if len(_channels) == 0:
        pygame.mixer.set_num_channels(40)
        for _ in range(1, 20):
            _channels.append(pygame.mixer.Channel(_))

    if snd_name not in _sound_registry:
        _sound_registry[snd_name] = pygame.mixer.Sound(join("assets", snd_name))

    chan = pygame.mixer.find_channel(False)
    if not chan:
        return False
    if chan.get_busy():
        return False
    chan.set_volume(vol)
    chan.play(_sound_registry[snd_name])
    return True


def interpolate_fn(n):
    """Interpolate sigmoidally from 0-1"""
    n = min(max(n, 0), 1)

    return sin(pi * (n - 0.5)) / 2 + 0.5
