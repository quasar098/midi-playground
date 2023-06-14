#!/usr/bin/env python3

import argparse


def main():
    parser = argparse.ArgumentParser(
            prog='./main.py',
            description='Bounce the squares!',
            epilog='Example: python3 main.py ./samples/cruel-angels-thesis-mainlines.mid -m ./samples/cruel-angels-thesis.mid'
    )
    parser.add_argument('infile', help="MIDI file to read in from and put the notes there")
    parser.add_argument('-m', '--music', help='Music file. Can be a MIDI (tested), an mp3 (tested), or a wav (untested)')
    parser.add_argument('-c', '--camera', default=2, type=int, help='Camera mode (0=static, 1=lazy, 2=smooth, 3=predictive). Default is 2')
    parser.add_argument('-n', '--notes', type=int, help='Max number of notes (timestamps) to calculate for. Default is infinity')
    parser.add_argument('-d', '--delay', type=float, help='Mi= 0.05')
    parser.add_argument('-s', '--square-speed', type=int, default=500, help="Square speed in pixels per second. Default = 500")
    parser.add_argument('-v', '--volume', type=int, default=50, help="Volume out of 100. Default = 50")
    parser.add_argument('-l', '--last', type=float, default=1, help="Last bounce offset time. Default = 1")
    parser.add_argument('--hallway', action='store_true', help="Enable this flag for hallway mode. Default = off")
    parser.add_argument("-b", '--backtrack-chance', type=float, default=0.03, help="Chance to backtrack on failure. Default = 0.03")
    parser.add_argument("-B", '--backtrack-amount', type=int, default=20, help="Steps to backtrack on failure. Default = 20")
    parser.add_argument('-o', '--offset', type=int, default=-300, help="Music offset in millis. Positive is music is delayed. " +
                                                                       "Negative is music is first. Default = -300")
    parser.add_argument('-t', '--theme', type=str, default="dark", help="Theme to use. Default = dark")
    parser.add_argument('-a', '--anim', type=int, default=1, help="Animation mode. 0 = off, 1 = on. Default = 1")
    parser.add_argument('-p', '--particles', type=int, default=1, help="Particle mode. 0 = off, 1 = on. Default = 1")


    ns = parser.parse_args()
    from bouncegen import do_the_things as do_bouncing
    raw_bounce_args = {
        "midi_file_name": ns.infile,
        "audio_file": ns.music,
        "camera_mode": ns.camera,
        "max_notes": ns.notes,
        "bounce_min_space": ns.delay,
        "sq_speed": ns.square_speed,
        "volume": ns.volume,
        "music_offset": ns.offset,
        "percent_chance_dir_change": 30 if not ns.hallway else 10,
        "backtrack_chance": ns.backtrack_chance,
        "backtrack_amount": ns.backtrack_amount,
        "theme": ns.theme,
        "anim": ns.anim,
        "draw_particles": ns.particles,
    }
    filtered_args = {}
    for k, v in raw_bounce_args.items():
        if v is not None:
            filtered_args[k] = v
    do_bouncing(filtered_args)


if __name__ == "__main__":
    main()


