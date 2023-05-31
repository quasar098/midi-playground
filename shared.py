import mido
from os import environ
from sys import platform
from enum import Enum
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # so you can pipe output from bouncegen.py to file safely


try:
    import win32api
    FRAMERATE = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1).DisplayFrequency
except ModuleNotFoundError:
    if platform == "win32":
        print("The win32api python module is not found! Install it with \"pip install pywin32\"")
    FRAMERATE = 60


class CameraFollow(Enum):
    Centre = 0
    Lazy = 1
    Smoothed = 2
    Predictive = 3


# noinspection PyUnresolvedReferences
def read_midi_file(filename):
    mid = mido.MidiFile(filename)

    _notes = []
    current_time = 0
    _instruments = {}
    now_channel = 2
    skip_first_meta = True

    for msg in mid:
        if isinstance(msg, mido.MetaMessage):
            if msg.type == 'track_name':
                if skip_first_meta:
                    skip_first_meta = False
                    continue
                _instruments[now_channel] = msg.name
        if msg.type == "program_change":
            now_channel = msg.channel
        if msg.type == 'note_on' and msg.velocity != 0:
            _note = msg.note
            _time = current_time + msg.time
            _notes.append((_note, round(_time*100)/100, msg.channel))

        current_time += msg.time

    return _instruments, _notes
