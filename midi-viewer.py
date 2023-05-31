from shared import *
import pygame
from sys import argv


WIDTH, HEIGHT = 1280, 720
START_OFFSET = 410
LINE_OFFSET = 400
NOTE_SPEED = 500
INSTRUMENT_COLORS = {
    0: (255, 128, 0),
    1: (128, 128, 255),
    2: (128, 255, 128),
    9: (0, 128, 255)
}


def main():
    midi_file_name = 'samples/cruel-angels-thesis.mid' if len(argv) == 1 else argv[1]
    instruments, notes = read_midi_file(midi_file_name)

    pygame.init()
    pygame.display.set_caption("midi viewer")
    pygame.mixer.init()

    pygame.mixer.music.load(midi_file_name)

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = pygame.time.Clock()

    pygame.mixer.music.play()

    y_scroll = 0
    goal_y_scroll = 0

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button > 3:
                    goal_y_scroll -= 50 * (event.button * 2 - 9)
                if event.button == 1:
                    print(round(pygame.time.get_ticks()/10)/100)

        y_scroll = (goal_y_scroll*0.1 + y_scroll*0.9)

        pygame.draw.line(screen, (255, 0, 0), (LINE_OFFSET, 0), (LINE_OFFSET, HEIGHT))
        for note in notes:
            x = note[1]*NOTE_SPEED - pygame.time.get_ticks()/1000*NOTE_SPEED
            y = HEIGHT-note[0]*20+500
            pos = (x + START_OFFSET + LINE_OFFSET, y + y_scroll)
            pygame.draw.circle(screen, INSTRUMENT_COLORS.get(note[2], (255, 0, 0)), pos, 10)

        pygame.display.flip()
        clock.tick(FRAMERATE)
    pygame.quit()


if __name__ == '__main__':
    main()
