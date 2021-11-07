import time
import curses
import asyncio
import random

TIC_TIMEOUT = 0.1


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


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


def draw(canvas):
    rows_count, columns_count = curses.window.getmaxyx(canvas)
    stars_count = int(rows_count * columns_count / 30)
    canvas.border()
    curses.curs_set(False)
    blink_coroutines = []
    fire_coroutine = fire(canvas, random.randint(1, rows_count-2), random.randint(1, columns_count-2))
    blink_coroutines.append(fire_coroutine)
    for _ in range(stars_count):
        row = random.randint(1, rows_count-2)
        column = random.randint(1, columns_count-2)
        symbol = random.choice('+*.:')
        blink_coroutine = blink(canvas, row, column, symbol)
        blink_coroutines.append(blink_coroutine)
    while True:
        try:
            for coroutine in blink_coroutines:
                coroutine.send(None)
        except StopIteration:
            blink_coroutines.remove(coroutine)
            canvas.border()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
