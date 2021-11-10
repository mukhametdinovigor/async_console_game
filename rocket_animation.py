import curses
import asyncio

from itertools import cycle
from curses_tools import draw_frame, read_controls

ROCKET_SPEED = 1
ROCKET_HEIGHT = 10
ROCKET_WIDTH = 6


async def animate_spaceship(canvas, row, column, frames, speed=ROCKET_SPEED):
    rows_count, columns_count = curses.window.getmaxyx(canvas)
    for frame in cycle(frames):
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame, negative=True)

        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        if row < 1:
            row = 1
        elif row > (rows_count - ROCKET_HEIGHT):
            row = rows_count - ROCKET_HEIGHT
        elif column < 1:
            column = 1
        elif column > (columns_count - ROCKET_WIDTH):
            column = columns_count - ROCKET_WIDTH
        else:
            row += rows_direction * speed
            column += columns_direction * speed
