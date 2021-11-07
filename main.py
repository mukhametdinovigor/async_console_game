import time
import curses
import asyncio
import random

TIC_TIMEOUT = 0.1


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
    coroutines = []
    for _ in range(stars_count):
        row = random.randint(1, rows_count-2)
        column = random.randint(1, columns_count-2)
        symbol = random.choice('+*.:')
        coroutine = blink(canvas, row, column, symbol)
        coroutines.append(coroutine)
    while True:
        for coroutine in coroutines:
            coroutine.send(None)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
