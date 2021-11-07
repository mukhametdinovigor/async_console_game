import time
import curses
import asyncio
import random

from itertools import cycle
from fire_animation import fire
from curses_tools import draw_frame, read_controls

TIC_TIMEOUT = 0.1


def get_rocket_frames():
    with open("frames/rocket_frame_1.txt", "r") as frame_1:
        rocket_frame_1 = frame_1.read()
    with open("frames/rocket_frame_2.txt", "r") as frame_2:
        rocket_frame_2 = frame_2.read()
    return rocket_frame_1, rocket_frame_2


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(random.randint(1, 20)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(random.randint(1, 3)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(random.randint(1, 5)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(random.randint(1, 3)):
            await asyncio.sleep(0)


async def animate_spaceship(canvas, row, column, frames):

    for frame in cycle(frames):
        canvas.nodelay(True)
        draw_frame(canvas, row, column, frame)
        canvas.refresh()
        await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame, negative=True)
        await asyncio.sleep(0)
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        row += rows_direction
        column += columns_direction
        canvas.border()


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
    canvas.border()
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
        draw_items(rocket_coroutines, canvas, timer=0)
        draw_items(blink_coroutines, canvas, TIC_TIMEOUT)
        draw_items(fire_coroutines, canvas, timer=0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
