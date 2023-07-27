# noinspection PyUnresolvedReferences
from typing import Union, Optional, BinaryIO
# noinspection PyUnresolvedReferences
from errors import *
from config import Config, get_colors
# noinspection PyUnresolvedReferences
from time import time as get_current_time
import moderngl
import mido
import pygame
from sys import platform
import subprocess
from enum import Enum
from os.path import join
from math import sin, pi
from sys import setrecursionlimit
setrecursionlimit(10000)  # increase if more notes


# vsync framerate if on windows, else 60
if platform == "win32":
    try:
        # noinspection PyPackageRequirements
        import win32api
        FRAMERATE = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1).DisplayFrequency
    except ModuleNotFoundError:
        print("The win32api python module is not found! Install it with \"pip install pywin32\"")
        FRAMERATE = 60
elif "linux" in platform:
    # noinspection PyPackageRequirements
    from Xlib import display
    # noinspection PyPackageRequirements
    from Xlib.ext import randr
    d = display.Display()
    default_screen = d.get_default_screen()
    info = d.screen(default_screen)

    resources = randr.get_screen_resources(info.root)
    active_modes = set()
    for crtc in resources.crtcs:
        crtc_info = randr.get_crtc_info(info.root, crtc, resources.config_timestamp)
        if crtc_info.mode:
            active_modes.add(crtc_info.mode)

    for mode in resources.modes:
        if mode.id in active_modes:
            FRAMERATE = round(mode.dot_clock / (mode.h_total * mode.v_total))
            break
else:
    FRAMERATE = 60


# camera follow modes
class CameraFollow(Enum):
    Center = 0  # center the square
    Lazy = 1  # lazy camera, used by Crazy Nutter 101
    Smoothed = 2  # smoothed camera, interpolates camera a little bit between current and previous every frame
    Predictive = 3  # smoothed camera, but you can see where the square will bounce better


def read_osu_file(filedata: bytes):
    filedata = filedata.decode("utf-8")
    filelines = filedata.splitlines(False)
    started_counting = False
    timestamps = []
    for line in filelines:
        if not started_counting:
            if "HitObjects" in line:
                started_counting = True
            continue
        if len(line) < 3:
            continue
        args = line.split(",")
        if (int(args[3]) & 3) == 0:
            continue
        timestamps.append(int(args[2])/1000)
    return timestamps


def surf_to_texture(in_surface: pygame.Surface) -> moderngl.Texture:
    tex = Config.ctx.texture(in_surface.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(in_surface.get_view('1'))
    return tex


def update_screen(screen: pygame.Surface, glsl_program: moderngl.Program, render_object: moderngl.VertexArray):
    frame_tex = surf_to_texture(screen)
    frame_tex.use(0)
    glsl_program['tex'] = 0
    if "ascii.glsl" in Config.shader_file_name:
        if Config.ascii_tex is None:
            Config.ascii_tex = surf_to_texture(pygame.image.load('./assets/shaders/ascii.png').convert_alpha())
            Config.ascii_tex.use(1)
        try:
            glsl_program['asciipng'] = 1
        except KeyError:
            pass
    render_object.render(mode=moderngl.TRIANGLE_STRIP)

    pygame.display.flip()

    frame_tex.release()


def open_file(filename):
    if platform == "win32":
        from os import startfile
        startfile(filename)
    else:
        opener = "open" if platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


# noinspection PyUnresolvedReferences
def read_midi_file(file):
    midi_file = mido.MidiFile(file=file)

    notes = []
    current_time = 0

    for msg in midi_file:
        if msg.type == 'note_on' and msg.velocity != 0:
            timestamp = current_time + msg.time
            notes.append(round(timestamp*1000)/1000)
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


def fix_overlap(rects: list[pygame.Rect], callback=None):
    if callback is None:
        callback = lambda _: None
    xvs = set()
    yvs = set()
    for rect in rects:
        xvs.add(rect.right)
        xvs.add(rect.left)
        yvs.add(rect.top)
        yvs.add(rect.bottom)
    xvs = sorted(list(xvs))
    yvs = sorted(list(yvs))

    outputs = []
    for xv1 in range(len(xvs)-1):
        xv2 = xv1+1
        for yv1 in range(len(yvs)-1):
            yv2 = yv1+1
            r = pygame.Rect(xvs[xv1], yvs[yv1], xvs[xv2]-xvs[xv1], yvs[yv2]-yvs[yv1])
            if r.collidelist(rects)+1:
                outputs.append(r)

        callback(f"Checking minirectangles ({int(100*xv1*len(yvs)/(len(xvs)*len(yvs)))}% done)")

    callback("Merging adjacent minirectangles")

    for ai in range(len(outputs)-1):
        a = outputs[ai+1]
        b = outputs[ai]
        if a.width == 0 or a.height == 0 or b.width == 0 or b.height == 0:
            continue
        if not (a.right == b.left or a.left == b.right or a.top == b.bottom or b.bottom == a.top):
            continue
        if a.x == b.x and a.width == b.width:
            a.y = min(a.y, b.y)
            a.height = a.height+b.height
            b.height = 0
            continue

    outputs = [out for out in outputs if out.width > 0 and out.height > 0]

    outputs.sort(key=lambda _: _.y*100000+_.x)

    for ai in range(len(outputs)-1):
        a = outputs[ai+1]
        b = outputs[ai]
        if a.width == 0 or a.height == 0 or b.width == 0 or b.height == 0:
            continue
        if not (a.right == b.left or a.left == b.right or a.top == b.bottom or b.bottom == a.top):
            continue
        if a.y == b.y and a.height == b.height:
            a.x = min(a.x, b.x)
            a.width = a.width+b.width
            b.width = 0
            continue

    callback("Finished loading")

    return [out for out in outputs if out.width > 0 and out.height > 0]


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
