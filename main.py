import time
import curses
import asyncio


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


def draw(canvas):
    row, column = (10, 30)
    canvas.border()
    curses.curs_set(False)
    coroutines = []
    for column_position in range(column, column + 25, 5):
        coroutine = blink(canvas, row, column_position, symbol='*')
        coroutines.append(coroutine)
    while True:
        for coroutine in coroutines:
            coroutine.send(None)
        canvas.refresh()
        time.sleep(0.1)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
