from pygame import init
from pygame.display import set_mode, flip
from pygame.time import Clock
from pygame.event import get
from pygame import QUIT
from time import perf_counter_ns
import src.Settings as Settings
from src.FPS import Fps
from src.board.Board import Board

init()
screen = set_mode(Settings.size)
clock = Clock()

Fps_counter = Fps(1)

board = Board([Settings.size[0]/2, Settings.size[1]/2])

running = True

dt = 0.016
while running:

    start = perf_counter_ns()

    screen.fill((0,0,0))

    events = get()
    for event in events:
        if event.type == QUIT:
            running = False

    board.update(screen, events)
    Fps_counter.update(screen, dt)

    flip()
    clock.tick(60)

    dt = (perf_counter_ns() - start) / 1_000_000_000