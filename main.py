#!/usr/bin/env python3

import argparse


def main():
    parser = argparse.ArgumentParser(
            prog='./main.py',
            description='Bounce the squares!',
            epilog='Example: python3 main.py ./samples/cruel-angels-thesis-mainlines.mid -m ./samples/cruel-angels-thesis.mid'
    )
    parser.add_argument('infile', help="MIDI file to read in from and put the notes there")
    parser.add_argument('-m', '--music', help='Music file. Can be a MIDI (tested), an mp3 (untested), or a wav (untested)')
    parser.add_argument('-c', '--camera', default=2, type=int, help='Camera mode (0=static, 1=lazy, 2=smooth). Default is 2')
    parser.add_argument('-n', '--notes', type=int, help='Max number of notes (timestamps) to calculate for. Default is infinity')
    parser.add_argument('-d', '--delay', type=float, help='Minimum delay between bounces. Default = 0.05')
    parser.add_argument('-s', '--squarespeed', type=int, default=500, help="Square speed in pixels per second. Default = 500")
    parser.add_argument('-v', '--volume', type=int, default=50, help="Volume out of 100. Default = 50")
    parser.add_argument('-o', '--offset', type=int, default=0, help="Music offset in millis. Positive is music is delayed. " +
                                                                    "Negative is music is first. Default = 0")
    ns = parser.parse_args()
    music = ns.music if ns.music is not None else ns.infile
    from bouncegen import do_the_things as do_bouncing
    do_bouncing(ns.infile, music, ns.camera, ns.notes, ns.delay, ns.squarespeed, ns.volume, ns.offset)


if __name__ == "__main__":
    main()


