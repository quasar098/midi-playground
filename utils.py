from typing import Union, Optional
import mido
import pygame
from sys import platform
from enum import Enum
from config import Config
from sys import setrecursionlimit
setrecursionlimit(10000)  # increase if more notes


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
def remove_too_close_values(lst: list[float], threshold=0.03) -> list[float]:
    """Assumes the list is sorted"""
    new = []
    before = None
    for _ in lst:
        if before is None:
            before = _
            new.append(_)
            continue
        if before+threshold > _:
            continue
        before = _
        new.append(_)
    return new


def debug_rect(rect: pygame.Rect):
    """Print a copy-pastable equation for debugging in desmos graphing calculator"""
    print(f"\\operatorname\x7Bpolygon\x7D({rect.topleft}, {rect.topright}, {rect.bottomright}, {rect.bottomleft})")
