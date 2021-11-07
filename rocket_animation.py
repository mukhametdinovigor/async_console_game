import curses
import asyncio

from itertools import cycle
from curses_tools import draw_frame, read_controls

ROCKET_SPEED = 1


async def animate_spaceship(canvas, row, column, frames, speed=ROCKET_SPEED):
    rows_count, columns_count = curses.window.getmaxyx(canvas)
    for frame in cycle(frames):
        canvas.nodelay(True)
        draw_frame(canvas, row, column, frame)
        canvas.refresh()
        await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame, negative=True)
        await asyncio.sleep(0)
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        if row < 1:
            row = 1
        elif row > (rows_count - 10):
            row = rows_count - 10
        elif column < 1:
            column = 1
        elif column > (columns_count - 6):
            column = columns_count - 6
        else:
            row += rows_direction * speed
            column += columns_direction * speed
        canvas.border()
