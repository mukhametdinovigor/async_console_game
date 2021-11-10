import curses
import time
import random

from fire_animation import fire
from rocket_animation import animate_spaceship
from star_animation import blink

TIC_TIMEOUT = 0.1


def get_rocket_frames():
    with open("frames/rocket_frame_1.txt", "r") as frame_1:
        rocket_frame_1 = frame_1.read()
    with open("frames/rocket_frame_2.txt", "r") as frame_2:
        rocket_frame_2 = frame_2.read()
    return rocket_frame_1, rocket_frame_2


def draw_items(coroutines, canvas, timer):
    try:
        for coroutine in coroutines.copy():
            coroutine.send(None)
        time.sleep(timer)
    except StopIteration:
        coroutines.remove(coroutine)
        canvas.border()


def draw(canvas):
    rows_count, columns_count = curses.window.getmaxyx(canvas)
    stars_count = int(rows_count * columns_count / 50)
    frames = get_rocket_frames()
    curses.curs_set(False)

    rocket_coroutines = [animate_spaceship(canvas,
                                           int(rows_count / 2),
                                           int(columns_count / 2),
                                           frames)]
    blink_coroutines = []
    fire_coroutines = [fire(canvas, int(rows_count / 2), int(columns_count / 2) + 2)]

    for _ in range(stars_count):
        row = random.randint(1, rows_count-2)
        column = random.randint(1, columns_count-2)
        symbol = random.choice('+*.:')
        blink_coroutine = blink(canvas, row, column, symbol)
        blink_coroutines.append(blink_coroutine)
    while True:
        draw_items(blink_coroutines, canvas, TIC_TIMEOUT)
        draw_items(rocket_coroutines, canvas, timer=0)
        draw_items(fire_coroutines, canvas, timer=0)
        canvas.nodelay(True)
        canvas.border()
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
