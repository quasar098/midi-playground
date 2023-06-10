#!/usr/bin/env python3

import argparse
from random import randint as rand
from config import Config


def main():
    parser = argparse.ArgumentParser(
            prog='./cli.py',
            description='Bounce the squares!',
            epilog='Example: python3 cli.py ./samples/cruel-angels-thesis-mainlines.mid -m ./samples/cruel-angels-thesis.mid'
    )
    parser.add_argument('infile', help="MIDI file to read in from and put the notes there")
    parser.add_argument('-D', '--direction-change-chance', default=30, type=int, help="Chance that the bounce direction changes. Default = 30")
    parser.add_argument('-m', '--music', help='Music file. Can be a MIDI (tested), an mp3 (tested), or a wav (untested)')
    parser.add_argument('-c', '--camera', default=2, type=int, help='Camera mode (0=static, 1=lazy, 2=smooth, 3=predictive). Default is 2')
    parser.add_argument('-d', '--delay', default=0.03, type=float, help='Minimum delay between bounces. Default = 0.03')
    parser.add_argument('-s', '--square-speed', type=int, default=500, help="Square speed in pixels per second. Default = 500")
    parser.add_argument('-v', '--volume', type=int, default=50, help="Volume out of 100. Default = 50")
    parser.add_argument('-l', '--last-bounce-delay', type=float, default=1, help="Last bounce offset time to regain your bearings. Default = 1")
    parser.add_argument('-n', '--notes', type=int, help='Max number of notes (timestamps) to calculate for. Default is infinity')
    parser.add_argument("-b", '--backtrack-chance', type=float, default=0.01, help="Chance to backtrack on failure. Default = 0.01")
    parser.add_argument("-B", '--backtrack-amount', type=int, default=20, help="Steps to backtrack on failure. Default = 20")
    parser.add_argument("-S", '--seed', type=int, default=rand(15, 16423), help="Map seed value. Default is a random number from 15 to 16423")
    parser.add_argument('-o', '--offset', type=int, default=-300, help="Music offset in millis. Positive is music is delayed. " +
                                                                       "Negative is music is first. Default = -300")

    ns = parser.parse_args()
    Config.seed = ns.seed
    Config.midi_file_name = ns.infile
    Config.audio_file_name = ns.infile if ns.music is None else ns.music
    Config.camera_mode = ns.camera
    Config.max_notes = ns.notes
    Config.bounce_min_spacing = ns.delay
    Config.square_speed = ns.square_speed
    Config.volume = ns.volume
    Config.music_offset = ns.offset
    Config.direction_change_chance = ns.direction_change_chance
    Config.backtrack_chance = ns.backtrack_chance
    Config.backtrack_amount = ns.backtrack_amount
    Config.last_bounce_delay = ns.last_bounce_delay

    from main import do_bouncing
    do_bouncing()


if __name__ == "__main__":
    main()
